"""Type B · 의사결정/위험 — clone-and-go 보일러플레이트 (mock 즉시 실행)
실행: streamlit run stack/templates/decision_app.py
LLM 연결은 ../streamlit_template.py 의 recommend() 패턴 참고."""
import streamlit as st

st.set_page_config(page_title="위험도 안내", page_icon="⚠️", layout="centered")

DEFAULTS = {"region": "서울", "hazard": "호우", "household": [], "result": None}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# 고정 데이터(예: 재난 행동요령) — data-patterns/로 분리 가능
GUIDE = {
    "호우": [("침수 우려 지역 즉시 대피", "High", "저지대·지하 이동"),
             ("하천·계곡 접근 금지", "High", "급류 위험"),
             ("배수구·맨홀 주의", "Med", "보행 시 우회")],
    "폭염": [("취약 시간 외출 자제", "High", "낮 12–17시"),
             ("수분 규칙적 섭취", "Med", "갈증 전에"),
             ("독거·고령 안부 확인", "High", "취약계층 점검")],
}
SIG = {"High": "🔴", "Med": "🟠", "Low": "🟢"}

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
        st.session_state.result = GUIDE[st.session_state.hazard]
        s.update(label="완료", state="complete")

res = st.session_state.result
if res:
    st.subheader(f"{st.session_state.region} · {st.session_state.hazard} 행동 계획")
    for action, risk, why in res:
        with st.container(border=True):
            st.markdown(f"{SIG[risk]} **{action}** — {why}  \n위험도 `{risk}`")
    text = "\n".join(f"- [{r}] {a}: {w}" for a, r, w in res)
    st.download_button("행동계획 다운로드(.md)", f"# {st.session_state.hazard} 행동계획\n{text}\n", "plan.md")
    st.info("다음 행동: 가족과 공유 → 대피경로 확인 → 비상용품 점검")
else:
    st.info("👆 지역·상황을 고르고 버튼을 누르세요. (예: 서울·호우)")
