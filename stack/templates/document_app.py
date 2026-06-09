"""Type D · 문서 생성 — clone-and-go (LLM 연결, 키 없으면 mock)
실행: streamlit run stack/templates/document_app.py"""
import os
import streamlit as st

MODEL = "claude-sonnet-4-6"
st.set_page_config(page_title="문서 초안", page_icon="📝", layout="centered")

DEFAULTS = {"dtype": "민원 신청", "org": "○○구청", "facts": "", "draft": None}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

def _key():
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    if not k:
        try:
            k = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            k = ""
    return k

def _mock(dtype, org, facts):
    body = "\n".join(f"- {ln}" for ln in facts.splitlines() if ln.strip()) or "- [______]"
    return (f"# {dtype}\n\n수신: {org}\n\n아래와 같이 {dtype}합니다.\n\n"
            f"## 내용\n{body}\n\n## 요청 사항\n[______]\n\n작성일: [____.__.__]\n신청인: [______]\n")

def draft_doc(dtype, org, facts):
    key = _key()
    if not key:
        return _mock(dtype, org, facts)
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        prompt = (f"<instructions>주어진 사실로 '{dtype}' 초안을 한국어 공문 톤(정중·명확·간결)으로 작성. "
                  "사실에 없는 내용은 지어내지 말고 빈칸은 [______]로 표시.</instructions>\n"
                  f"<doc_type>{dtype}</doc_type>\n<org>{org}</org>\n<facts>{facts}</facts>\n"
                  "출력: 마크다운 문서 본문(수신·내용·요청·서명).")
        m = c.messages.create(model=MODEL, max_tokens=1200, messages=[{"role": "user", "content": prompt}])
        return m.content[0].text
    except Exception as e:
        st.warning(f"LLM 실패 → mock: {e}")
        return _mock(dtype, org, facts)

st.title("📝 문서 초안 생성 (데모)")
st.caption("사안과 핵심 사실을 입력하면 문서 초안을 만들어 드립니다.")

types = ["민원 신청", "지원 신청서", "보고서"]
st.session_state.dtype = st.selectbox("문서 유형", types, index=types.index(st.session_state.dtype))
st.session_state.org = st.text_input("대상 기관", st.session_state.org)
st.session_state.facts = st.text_area("핵심 사실(한 줄씩)", st.session_state.facts,
                                      placeholder="예: 보도블록 파손 / 위치 ○○로 12 / 통행 위험")

if st.button("초안 생성", type="primary"):
    with st.status("작성 중…") as s:
        st.session_state.draft = draft_doc(st.session_state.dtype, st.session_state.org, st.session_state.facts)
        s.update(label="완료", state="complete")

draft = st.session_state.draft
if draft:
    edited = st.text_area("초안(편집 가능)", draft, height=320)
    st.download_button("문서 다운로드(.md)", edited, "document.md")
    st.info("다음 행동: 빈칸 [______] 채우고 → 해당 기관에 제출")
else:
    st.info("👆 유형·기관·사실을 입력하고 버튼을 누르세요.")
