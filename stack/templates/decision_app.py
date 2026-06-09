"""Type B · 의사결정/위험 — clone-and-go (LLM 연결, 키 없으면 mock)
실행: streamlit run stack/templates/decision_app.py
키: ANTHROPIC_API_KEY (env 또는 .streamlit/secrets.toml)"""
import os, json
import streamlit as st

MODEL = "claude-sonnet-4-6"
st.set_page_config(page_title="위험도 안내", page_icon="⚠️", layout="centered")

DEFAULTS = {"region": "서울", "hazard": "호우", "household": [], "result": None}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# 고정 데이터(예: 재난 행동요령) — data-patterns/로 분리 가능
GUIDE = {
    "호우": [{"action": "침수 우려 지역 즉시 대피", "risk": "High", "why": "저지대·지하 이동"},
             {"action": "하천·계곡 접근 금지", "risk": "High", "why": "급류 위험"},
             {"action": "배수구·맨홀 주의", "risk": "Med", "why": "보행 시 우회"}],
    "폭염": [{"action": "취약 시간 외출 자제", "risk": "High", "why": "낮 12–17시"},
             {"action": "수분 규칙적 섭취", "risk": "Med", "why": "갈증 전에"},
             {"action": "독거·고령 안부 확인", "risk": "High", "why": "취약계층 점검"}],
}
SIG = {"High": "🔴", "Med": "🟠", "Low": "🟢"}

def _key():
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    if not k:
        try:
            k = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            k = ""
    return k

def assess(region, hazard, household):
    base = GUIDE.get(hazard, [])
    key = _key()
    if not key:
        return base  # mock
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        prompt = ("<instructions>상황에 맞는 위험도(High/Med/Low)와 즉시 행동을 JSON 배열로. "
                  "단정적 판정 금지, data 밖은 지어내지 말 것.</instructions>\n"
                  f"<situation>지역:{region} / 상황:{hazard} / 가족:{household}</situation>\n"
                  f"<data>{json.dumps(base, ensure_ascii=False)}</data>\n"
                  'JSON: [{"action","risk","why"}]')
        m = c.messages.create(model=MODEL, max_tokens=800, messages=[{"role": "user", "content": prompt}])
        t = m.content[0].text
        return json.loads(t[t.find("["): t.rfind("]") + 1])
    except Exception as e:
        st.warning(f"LLM 실패 → mock: {e}")
        return base

st.title("⚠️ 우리 동네 위험 안내 (데모)")
st.caption("지역과 상황을 고르면 위험도와 지금 할 일을 정리해 드립니다.")

regions = ["서울", "경기", "부산", "기타"]
st.session_state.region = st.selectbox("지역", regions, index=regions.index(st.session_state.region))
hazards = list(GUIDE)
st.session_state.hazard = st.selectbox("상황", hazards, index=hazards.index(st.session_state.hazard))
st.session_state.household = st.multiselect("가족 구성(선택)", ["영유아", "고령", "반려동물", "장애"],
                                            default=st.session_state.household)

if st.button("위험도·행동 보기", type="primary"):
    with st.status("상황 분석 중…", expanded=True) as s:
        st.write("위험 평가")
        st.session_state.result = assess(st.session_state.region, st.session_state.hazard, st.session_state.household)
        s.update(label="완료", state="complete")

res = st.session_state.result
if res:
    st.subheader(f"{st.session_state.region} · {st.session_state.hazard} 행동 계획")
    for r in res:
        with st.container(border=True):
            st.markdown(f"{SIG.get(r.get('risk'), '🟢')} **{r.get('action', '')}** — {r.get('why', '')}  \n위험도 `{r.get('risk', '')}`")
    text = "\n".join(f"- [{r.get('risk')}] {r.get('action')}: {r.get('why')}" for r in res)
    st.download_button("행동계획 다운로드(.md)", f"# {st.session_state.hazard} 행동계획\n{text}\n", "plan.md")
    st.info("다음 행동: 가족과 공유 → 대피경로 확인 → 비상용품 점검")
else:
    st.info("👆 지역·상황을 고르고 버튼을 누르세요. (예: 서울·호우)")
