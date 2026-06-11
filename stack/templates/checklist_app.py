"""Type C · 체크리스트/준비 — clone-and-go (키 불필요 — 기한 계산은 전부 코드)
실행: streamlit run stack/templates/checklist_app.py

C형 기본값(★ patterns/checklist.md — 도메인을 바꿔도 이 메커니즘은 유지하라):
  ⓐ 기한 = 정적 문자열("D-200") ❌ → 기준일 + deadline_days로 '계산된' D-day·상태색(지남/임박/여유)
  ⓑ 진행률 + '지금 할 일 1개'(가장 급한 미완료) — 완료하면 다음으로 자동 이동
  ⓒ 조건부 항목은 conditions[]로 동적 노출(해당없음=숨김, 분모도 변동)
  ⓓ 입력·완료는 session_state에 저장(Rule③). 완료 키는 인덱스가 아니라 항목 id에 묶는다."""
from datetime import date, timedelta
import streamlit as st

st.set_page_config(page_title="준비 체크리스트", page_icon="🗂️", layout="centered")

# 항목(도메인에 맞게 교체) — deadline_days: 기준일로부터 며칠 내(None=상시), conditions: 켠 조건과 겹칠 때만 노출
ITEMS = [
    {"id": "a", "task": "필수 절차 1 (기한 14일)", "deadline_days": 14, "where": "신청처 1", "why": "늦으면 불이익.", "conditions": []},
    {"id": "b", "task": "필수 절차 2 (기한 30일)", "deadline_days": 30, "where": "신청처 2", "why": "후속 절차의 전제.", "conditions": []},
    {"id": "c", "task": "상시 항목", "deadline_days": None, "where": "신청처 3", "why": "언제든 가능.", "conditions": []},
    {"id": "d", "task": "조건부 항목 (조건1일 때만)", "deadline_days": 60, "where": "신청처 4", "why": "해당자만.", "conditions": ["조건1"]},
]
CONDITIONS = ["조건1", "조건2"]


def compute_row(item, base, today, done):
    """ⓐ 기준일+규칙 → 기한일·D-day·상태색 (계산은 코드로)."""
    d = item["deadline_days"]
    if d is None:
        return {**item, "done": done, "has_deadline": False, "days_left": 0,
                "icon": "✅" if done else "🟢", "when": "상시"}
    deadline = base + timedelta(days=d)
    left = (deadline - today).days
    icon = "✅" if done else ("🔴" if left < 0 else "🟠" if left <= 7 else "🟢")
    when = (f"기한 {abs(left)}일 지남" if left < 0 else f"D-{left}") + f" ({deadline:%m/%d})"
    return {**item, "done": done, "has_deadline": True, "days_left": left, "icon": icon, "when": when}


def build_rows(items, active, base, today, done_map):
    rows = [compute_row(it, base, today, done_map.get(it["id"], False))
            for it in items if not it["conditions"] or set(it["conditions"]) & active]  # ⓒ
    rows.sort(key=lambda r: (r["done"], not r["has_deadline"], r["days_left"]))  # 미완료·급한 순
    return rows


st.title("🗂️ 준비 체크리스트 (데모)")
st.caption("기준일과 조건만 넣으면 **기한순 체크리스트** — 지난·임박 경고, 진행률, 지금 할 일 1개. (입력·완료 자동 저장)")

# ⓓ 입력은 keyed widget → 세션 유지
today = date.today()
base = st.date_input("기준일 (D-day 계산 축)", key="base", value=today)
active = {c for c in CONDITIONS if st.checkbox(c, key=f"cond_{c}")}
for it in ITEMS:
    st.session_state.setdefault(f"chk_{it['id']}", False)  # ⓓ 완료는 id 키

done_map = {it["id"]: st.session_state[f"chk_{it['id']}"] for it in ITEMS}
rows = build_rows(ITEMS, active, base, today, done_map)
done_n = sum(r["done"] for r in rows)

st.progress(done_n / len(rows) if rows else 0, text=f"진행 {done_n}/{len(rows)} 완료")  # ⓑ
pending = [r for r in rows if not r["done"]]
if pending:
    nxt = pending[0]
    with st.container(border=True):
        st.markdown(f"### 👉 지금 할 일: **{nxt['task']}**\n{nxt['icon']} **{nxt['when']}** · {nxt['where']}")
        st.caption(nxt["why"])
else:
    st.success("🎉 모든 항목 완료!")

overdue = [r for r in rows if r["has_deadline"] and r["days_left"] < 0 and not r["done"]]
if overdue:
    st.warning("⚠️ 기한 지남: " + ", ".join(r["task"] for r in overdue))

st.subheader("📋 전체 (기한 급한 순)")
for r in rows:
    c1, c2 = st.columns([0.08, 0.92])
    c1.checkbox("완료", key=f"chk_{r['id']}", label_visibility="collapsed")
    strike = "~~" if r["done"] else ""
    c2.markdown(f"{r['icon']} {strike}**{r['task']}**{strike} · {r['when']}  \n*{r['why']} · {r['where']}*")

md = "\n".join(f"- [{'x' if r['done'] else ' '}] {r['task']} — {r['when']} ({r['where']})" for r in rows)
st.download_button("체크리스트 다운로드(.md)", f"# 준비 체크리스트 (기준일 {base})\n{md}\n", "checklist.md")
st.info("다음 행동: 가장 급한 항목부터 처리 → 완료 체크(저장됨) → 다음 방문 때 이어서.")
