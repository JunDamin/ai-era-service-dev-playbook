"""Type C · 체크리스트/준비 — clone-and-go 보일러플레이트 (mock 즉시 실행)
실행: streamlit run stack/templates/checklist_app.py"""
import streamlit as st

st.set_page_config(page_title="준비 체크리스트", page_icon="🗂️", layout="centered")

DEFAULTS = {"topic": "임신·출산", "checked": {}}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# 고정 데이터(단계·시점) — data-patterns/로 분리 가능
PLAN = {
    "임신·출산": [("산모수첩 발급", "D-200"), ("정부 임신·출산 지원 신청", "D-180"),
                ("출산용품 준비", "D-60"), ("출생신고 서류 확인", "D-7")],
    "재난 대비": [("비상용품 키트 구성", "상시"), ("대피경로 확인", "상시"),
                ("가족 연락계획 수립", "상시"), ("취약계층 점검", "상시")],
}

st.title("🗂️ 준비 체크리스트 (데모)")
st.caption("상황을 고르면 시점별 준비 항목을 체크리스트로 만들어 드립니다.")

topics = list(PLAN)
st.session_state.topic = st.selectbox("상황", topics, index=topics.index(st.session_state.topic))
items = PLAN[st.session_state.topic]

st.subheader("체크리스트")
for i, (task, when) in enumerate(items):
    key = f"{st.session_state.topic}_{i}"
    st.session_state.checked[key] = st.checkbox(f"**{task}** · {when}",
                                                value=st.session_state.checked.get(key, False))

done = sum(st.session_state.checked.get(f"{st.session_state.topic}_{i}", False) for i in range(len(items)))
st.progress(done / len(items), text=f"{done}/{len(items)} 완료")

md = "\n".join(
    f"- [{'x' if st.session_state.checked.get(f'{st.session_state.topic}_{i}') else ' '}] {t} ({w})"
    for i, (t, w) in enumerate(items))
st.download_button("체크리스트 다운로드(.md)", f"# {st.session_state.topic} 준비\n{md}\n", "checklist.md")
st.info("다음 행동: 가장 가까운 시점 항목부터 처리하세요.")
