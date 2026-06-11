"""Type B · 의사결정/위험 — clone-and-go (LLM 연결, 키 없으면 mock)
실행: streamlit run stack/templates/decision_app.py
키: ANTHROPIC_API_KEY (env 또는 .streamlit/secrets.toml)

B형 기본값(★ patterns/decision.md — 도메인을 바꿔도 이 메커니즘은 유지하라):
  ⓐ 신호는 예/아니오/'모름' 트라이스테이트 — 모름=0이 아니라 위험 가산(미확인=리스크)
  ⓑ 못 판정해도 행동은 준다 — 모름→확인 행동, 적신호→대응 행동(확인처 링크)
  ⓒ 점수만 주지 말고 신호별 기여를 펼쳐라(왜 이 위험도인지)"""
import os, json
import streamlit as st

MODEL = "claude-sonnet-4-6"
st.set_page_config(page_title="위험 점검", page_icon="⚠️", layout="centered")

# 위험 신호(도메인에 맞게 교체) — bad=위험인 답, weight=적신호 가중, unknown_weight=모름 가산
SIGNALS = [
    {"id": "s1", "label": "신호 1 — 핵심 위험 조건인가요?", "bad": "예", "weight": 3, "unknown_weight": 2,
     "check": "확인처 1", "check_url": "https://example.go.kr", "action_bad": "①을 먼저 확인하고 …하세요."},
    {"id": "s2", "label": "신호 2 — 안전 전제가 갖춰졌나요?", "bad": "아니오", "weight": 2, "unknown_weight": 1,
     "check": "확인처 2", "check_url": "https://example.go.kr", "action_bad": "②를 보완한 뒤 진행하세요."},
    {"id": "s3", "label": "신호 3 — 부가 위험 요소가 있나요?", "bad": "예", "weight": 1, "unknown_weight": 1,
     "check": "확인처 3", "check_url": "https://example.go.kr", "action_bad": "③의 대응 조치를 확인하세요."},
]
THRESHOLDS = {"high": 4, "med": 2}
ANSWERS = ("예", "아니오", "모름")
LEVEL_UI = {"High": ("🔴", "위험 높음", "error"), "Med": ("🟠", "주의 필요", "warning"), "Low": ("🟢", "비교적 안전", "success")}


def score(answers):
    """ⓐ 모름=가산 · ⓒ 신호별 기여 반환. (산정은 코드로 — LLM은 설명만)"""
    contribs, total = [], 0
    for sig in SIGNALS:
        ans = answers.get(sig["id"], "모름")
        pts = sig["weight"] if ans == sig["bad"] else (sig["unknown_weight"] if ans == "모름" else 0)
        kind = "bad" if ans == sig["bad"] else ("unknown" if ans == "모름" else "safe")
        total += pts
        contribs.append({"sig": sig, "answer": ans, "points": pts, "kind": kind})
    level = "High" if total >= THRESHOLDS["high"] else ("Med" if total >= THRESHOLDS["med"] else "Low")
    contribs.sort(key=lambda c: c["points"], reverse=True)
    return {"total": total, "level": level, "contribs": contribs}


def build_actions(contribs):
    """ⓑ 모름→확인 행동, 적신호→대응 행동 (점수순)."""
    out = []
    for c in contribs:
        if c["kind"] == "bad":
            out.append({"tag": "대응", "text": c["sig"]["action_bad"], "check": c["sig"]["check"], "url": c["sig"]["check_url"]})
        elif c["kind"] == "unknown":
            out.append({"tag": "확인", "text": f"미확인 — {c['sig']['label']} 을(를) 확인처에서 직접 확인하세요.",
                        "check": c["sig"]["check"], "url": c["sig"]["check_url"]})
    return out


def _key():
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    if not k:
        try:
            k = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            k = ""
    return k


def explain(res):
    bad = [c for c in res["contribs"] if c["kind"] == "bad"]
    unk = [c for c in res["contribs"] if c["kind"] == "unknown"]
    fallback = (f"종합 위험도 '{res['level']}'(점수 {res['total']}). 적신호 {len(bad)}건, 미확인 {len(unk)}건 — "
                "미확인은 그 자체가 위험입니다. 확인 전까지 위험으로 간주하세요.")
    key = _key()
    if not key:
        return fallback
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        facts = [{"신호": x["sig"]["label"], "답": x["answer"], "기여": x["points"]} for x in res["contribs"]]
        m = c.messages.create(model=MODEL, max_tokens=300, messages=[{"role": "user", "content":
            ("<instructions>위험 점검 요약 2~3문장. 단정 판정 금지(확인 필요로), 지어내기 금지. "
             "'모름/미확인'은 안전이 아니라 위험으로 다뤄라.</instructions>\n"
             f"<level>{res['level']} {res['total']}</level>\n<signals>{json.dumps(facts, ensure_ascii=False)}</signals>")}])
        return (m.content[0].text or "").strip() or fallback
    except Exception:
        return fallback


st.title("⚠️ 위험 점검 (데모)")
st.caption("신호에 답하면 위험도·왜·지금 할 행동까지. **'모름'도 위험으로 계산**합니다(확인 안 함=리스크).")

for sig in SIGNALS:  # 입력은 세션 키로 저장(Rule③)
    st.radio(sig["label"], ANSWERS, key=f"sig_{sig['id']}", index=2, horizontal=True,
             help=f"확인처: {sig['check']}")

answers = {sig["id"]: st.session_state[f"sig_{sig['id']}"] for sig in SIGNALS}
res = score(answers)
icon, label, box = LEVEL_UI[res["level"]]
getattr(st, box)(f"## {icon} 종합 위험도: {label} · 점수 {res['total']}")
st.caption(explain(res))

with st.expander("왜 이 위험도인가요? (신호별 기여)", expanded=res["level"] != "Low"):  # ⓒ
    for c in res["contribs"]:
        mark = {"bad": "⚠️", "unknown": "❓", "safe": "✅"}[c["kind"]]
        st.write(f"{mark} {c['sig']['label']} — 답 `{c['answer']}` · 기여 **+{c['points']}**")

st.subheader("✅ 지금 할 행동 (우선순위순)")
actions = build_actions(res["contribs"])
for i, a in enumerate(actions, 1):
    with st.container(border=True):
        st.markdown(f"**{i}. [{a['tag']}] {a['text']}**")
        st.link_button(f"확인처: {a['check']}", a["url"])
if not actions:
    st.success("적신호·미확인이 없습니다.")

text = "\n".join(f"- [{a['tag']}] {a['text']} (확인처: {a['check']})" for a in actions)
st.download_button("점검 리포트 다운로드(.md)",
                   f"# 위험 점검\n위험도: {res['level']} (점수 {res['total']})\n\n{text}\n\n※ 법적 판정 아님 — 확인처에서 직접 확인.",
                   "risk_report.md")
st.info("다음 행동: 미확인 신호를 확인처에서 채움 → 위험도 재확인. (단정 판정 아님)")
