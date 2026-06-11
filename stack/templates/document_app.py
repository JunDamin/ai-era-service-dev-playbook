"""Type D · 문서 생성 — clone-and-go (LLM 연결, 키 없으면 mock)
실행: streamlit run stack/templates/document_app.py

D형 기본값(★ patterns/document.md — 생성형의 해자는 '글'이 아니라 그 주변):
  ⓐ 라우팅 — 유형을 고르게 하지 말고 상황 서술로 자동 분류(키워드 폴백) + 수정 가능
  ⓑ 갭점검 — 생성 전 필수 정보(needed)와 대조해 빠진 것 경고(반려 예방)
  ⓒ 효과화 — 사용자가 준 사실만 사용, 지어내기 금지, 빈칸은 [______]
  ※ D형은 자유 서술이 주입력(P6) — 구조 정보(위치·일시 등)만 전용 칸으로"""
import os
import streamlit as st

MODEL = "claude-sonnet-4-6"
st.set_page_config(page_title="문서 초안", page_icon="📝", layout="centered")

# 문서 유형(도메인에 맞게 교체) — keywords: 분류 폴백, needed: 갭점검 목록
DOC_TYPES = [
    {"type": "유형 1 (예: 시정 요청)", "org": "담당 기관 1", "keywords": ["파손", "고장", "수리"],
     "needed": ["위치", "발생 일시", "현장 사진"]},
    {"type": "유형 2 (예: 지원 신청)", "org": "담당 기관 2", "keywords": ["신청", "지원", "혜택"],
     "needed": ["신청인 정보", "자격 근거"]},
]


def classify(text):
    """ⓐ 상황 서술 → 유형 추정(키워드 폴백 — LLM 분류로 교체 가능)."""
    for d in DOC_TYPES:
        if any(k in (text or "") for k in d["keywords"]):
            return d, "확인 필요"
    return DOC_TYPES[0], "확인 필요"


def find_gaps(doc, situation, extra):
    """ⓑ needed와 대조 — 전용 입력칸이 있으면 그 칸 기준으로 점검."""
    blob = f"{situation} {extra}"
    return [n for n in doc["needed"] if not any(w in blob for w in n.split() if len(w) >= 2)]


def _key():
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    if not k:
        try:
            k = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            k = ""
    return k


def _mock(doc, situation, extra):
    body = "\n".join(f"- {ln}" for ln in f"{situation}\n{extra}".splitlines() if ln.strip()) or "- [______]"
    return (f"# {doc['type']}\n\n수신: {doc['org']}\n\n아래와 같이 요청드립니다.\n\n## 내용\n{body}\n\n"
            "## 요청 사항\n[______]\n\n작성일: [____.__.__]\n신청인: [______]\n")


def draft_doc(doc, situation, extra):
    key = _key()
    if not key:
        return _mock(doc, situation, extra)
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        m = c.messages.create(model=MODEL, max_tokens=1200, messages=[{"role": "user", "content":
            (f"<instructions>'{doc['type']}' 초안을 한국어 공문 톤(정중·명확·간결)으로. "
             "사용자가 준 사실만 사용 — 없는 사실·법조항·수치 지어내기 금지, 빈칸은 [______]. "
             "사실 범위에서 공익적 영향(안전·반복성)을 부각하고 요구사항은 구체·실행가능하게.</instructions>\n"
             f"<org>{doc['org']}</org>\n<facts>{situation}\n{extra}</facts>\n출력: 마크다운 문서 본문")}])
        return m.content[0].text
    except Exception as e:
        st.warning(f"LLM 실패 → mock: {e}")
        return _mock(doc, situation, extra)


st.title("📝 문서 초안 생성 (데모)")
st.caption("상황을 편하게 쓰면 **① 어떤 문서인지 판단 → ② 빠진 정보 점검 → ③ 초안**까지. (유형을 몰라도 OK)")

situation = st.text_area("상황 설명 (주입력 — 자유롭게)", key="situation",
                         placeholder="예: ○○에서 …한 문제가 반복되고 있어 조치가 필요합니다.")
extra = st.text_input("구조 정보 (위치·일시 등)", key="extra")

if st.button("분석하고 초안 만들기", type="primary") and situation.strip():
    doc, conf = classify(situation)  # ⓐ
    st.session_state.doc_pick = doc["type"]
    st.session_state.draft = None

if st.session_state.get("doc_pick"):
    names = [d["type"] for d in DOC_TYPES]
    pick = st.selectbox("문서 유형 (다르면 바꾸세요)", names, index=names.index(st.session_state.doc_pick))  # ⓐ 수정 가능
    doc = next(d for d in DOC_TYPES if d["type"] == pick)
    st.markdown(f"**접수처:** {doc['org']}")

    gaps = find_gaps(doc, situation, extra)  # ⓑ
    if gaps:
        st.warning("**반려 예방 — 빠진 정보:** " + " · ".join(gaps))
    else:
        st.info("✅ 필수 정보가 대체로 갖춰졌습니다.")

    if st.session_state.get("draft") is None:
        st.session_state.draft = draft_doc(doc, situation, extra)  # ⓒ
    edited = st.text_area("초안(편집 가능)", st.session_state.draft, height=320)
    st.download_button("문서 다운로드(.md)", edited, "document.md")
    st.info("다음 행동: 빠진 정보 보완 → 빈칸 [______] 채움 → 접수처 제출. (보조 도구 생성물 — 제출 전 확인)")
else:
    st.info("👆 상황을 쓰고 버튼을 누르세요.")
