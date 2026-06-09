"""
서비스 개발 플레이북 — Streamlit 단일파일 보일러플레이트 (clone-and-go)

실행:  pip install -r requirements.txt  &&  streamlit run stack/streamlit_template.py
- API 키 없어도 mock으로 즉시 동작 → 키(ANTHROPIC_API_KEY) 넣으면 실제 LLM.
- 이 파일은 lessons/ 원칙을 코드로 구현한 '중간 출발점'. 문제만 바꿔 끼우면 된다.
"""
import os, json
import streamlit as st

MODEL = "claude-sonnet-4-6"  # 앱은 보통 Sonnet으로 충분(복잡하면 opus)

# 0) 페이지 — 일관 디자인 (lessons/ux)
st.set_page_config(page_title="서비스 데모", page_icon="✅", layout="centered")

# 1) 세션 상태 + 자동저장 (lessons/defaults: autosave, 재입력 강요 금지)
DEFAULTS = {"region": "서울", "targets": [], "result": None}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# 2) 고정 샘플 데이터 (lessons/mvp: 실시간 API 의존 X → data-patterns/로 분리 가능)
SAMPLE = [
    {"name": "기초연금", "target": "65세 이상", "benefit": "월 최대 33만원",
     "how": "복지로/주민센터 신청", "docs": "신분증, 통장", "url": "https://www.bokjiro.go.kr"},
    {"name": "근로장려금", "target": "저소득 근로", "benefit": "연 최대 330만원",
     "how": "홈택스 신청", "docs": "소득자료", "url": "https://www.hometax.go.kr"},
]

def _get_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            key = ""
    return key

def recommend(profile: dict) -> list:
    """LLM 추천 — 키 없으면 mock. (자격 '판정' 금지, 데이터 밖은 지어내지 않음)"""
    key = _get_key()
    if not key:
        return [{**s, "confidence": "확인 필요", "why": "데모 mock (API 키 없음)"} for s in SAMPLE]
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        prompt = (
            "<instructions>아래 후보에서 사용자에게 맞는 항목을 골라 우선순위·confidence·이유를 JSON으로. "
            "자격 판정 금지, 데이터에 없는 건 지어내지 말 것(없으면 confidence='확인 필요').</instructions>\n"
            f"<user_profile>{json.dumps(profile, ensure_ascii=False)}</user_profile>\n"
            f"<candidates>{json.dumps(SAMPLE, ensure_ascii=False)}</candidates>\n"
            'JSON 배열만 출력: [{"name","benefit","how","docs","url","confidence","why"}]'
        )
        msg = client.messages.create(model=MODEL, max_tokens=1024,
                                     messages=[{"role": "user", "content": prompt}])
        text = msg.content[0].text
        return json.loads(text[text.find("["): text.rfind("]") + 1])
    except Exception as e:
        st.warning(f"LLM 호출 실패 → mock 사용: {e}")
        return [{**s, "confidence": "확인 필요", "why": "fallback"} for s in SAMPLE]

# 3) 헤더 — 무엇을 하는지 1줄
st.title("✅ 맞춤 혜택 찾기 (데모)")
st.caption("조건을 고르면 받을 수 있는 혜택과 신청 방법을 정리해 드립니다.")

# 4) 입력 — 선택 > 입력, 영구 레이블 (lessons/data-input)
regions = ["서울", "경기", "부산", "기타"]
st.session_state.region = st.selectbox("지역", regions, index=regions.index(st.session_state.region))
st.session_state.targets = st.multiselect(
    "대상 유형", ["65세 이상", "저소득 근로", "장애", "다문화"], default=st.session_state.targets)

# 5) 실행 — 빈 스피너 대신 진행 표시 (lessons/ai-chat)
if st.button("받을 수 있는 혜택 보기", type="primary"):
    with st.status("상황 분석 중…", expanded=True) as s:
        st.write("프로필 정리")
        profile = {"region": st.session_state.region, "targets": st.session_state.targets}
        st.write("후보 탐색")
        st.session_state.result = recommend(profile)
        s.update(label="완료", state="complete")

# 6) 결과 — 카드 + confidence + 복사/다운로드 + 다음 행동 (lessons/dashboard)
res = st.session_state.result
if res:
    st.subheader("추천 결과")
    for r in res:
        with st.container(border=True):
            st.markdown(
                f"**{r['name']}** · {r.get('benefit','')}  \n"
                f"신청: {r.get('how','')} · 서류: {r.get('docs','')}  \n"
                f"신뢰도: `{r.get('confidence','')}` — {r.get('why','')}")
            st.link_button("공식 페이지", r.get("url", "#"))
    summary = "\n".join(f"- {r['name']}: {r.get('benefit','')} / {r.get('how','')}" for r in res)
    st.text_area("복사용 요약", summary, height=120)
    st.download_button("체크리스트 다운로드(.md)", f"# 신청 체크리스트\n{summary}\n", "checklist.md")
    st.info("다음 행동: 위 '공식 페이지'에서 신청 → 서류 준비 → 제출")
else:
    # 빈 화면 금지 (lessons/ux): 안내 제공
    st.info("👆 조건을 고르고 버튼을 누르면 결과가 나옵니다. (예: 지역=서울, 대상=65세 이상)")
