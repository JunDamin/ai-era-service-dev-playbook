"""Type D · 문서 생성 — clone-and-go 보일러플레이트 (mock 즉시 실행)
실행: streamlit run stack/templates/document_app.py
LLM 연결 지점은 ../streamlit_template.py recommend() 패턴 참고."""
import streamlit as st

st.set_page_config(page_title="문서 초안", page_icon="📝", layout="centered")

DEFAULTS = {"dtype": "민원 신청", "org": "○○구청", "facts": "", "draft": None}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

st.title("📝 문서 초안 생성 (데모)")
st.caption("사안과 핵심 사실을 입력하면 문서 초안을 만들어 드립니다.")

types = ["민원 신청", "지원 신청서", "보고서"]
st.session_state.dtype = st.selectbox("문서 유형", types, index=types.index(st.session_state.dtype))
st.session_state.org = st.text_input("대상 기관", st.session_state.org)
st.session_state.facts = st.text_area("핵심 사실(한 줄씩)", st.session_state.facts,
                                      placeholder="예: 보도블록 파손 / 위치 ○○로 12 / 통행 위험")

if st.button("초안 생성", type="primary"):
    with st.status("작성 중…") as s:
        # LLM 연결 지점(여기선 템플릿 mock): 사실에 없는 건 [______]로 비움
        facts = "\n".join(f"- {ln}" for ln in st.session_state.facts.splitlines() if ln.strip()) or "- [______]"
        st.session_state.draft = (
            f"# {st.session_state.dtype}\n\n수신: {st.session_state.org}\n\n"
            f"아래와 같이 {st.session_state.dtype}합니다.\n\n## 내용\n{facts}\n\n"
            f"## 요청 사항\n[______]\n\n작성일: [____.__.__]\n신청인: [______]\n")
        s.update(label="완료", state="complete")

draft = st.session_state.draft
if draft:
    edited = st.text_area("초안(편집 가능)", draft, height=320)
    st.download_button("문서 다운로드(.md)", edited, "document.md")
    st.info("다음 행동: 빈칸 [______] 채우고 → 해당 기관에 제출")
else:
    st.info("👆 유형·기관·사실을 입력하고 버튼을 누르세요.")
