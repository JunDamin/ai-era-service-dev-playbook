"""Type C · 체크리스트/준비 — clone-and-go (LLM 연결, 키 없으면 mock)
실행: streamlit run stack/templates/checklist_app.py"""
import os, json
import streamlit as st

MODEL = "claude-sonnet-4-6"
st.set_page_config(page_title="준비 체크리스트", page_icon="🗂️", layout="centered")

DEFAULTS = {"topic": "임신·출산", "items": None, "checked": {}}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# 고정 데이터(단계·시점) — data-patterns/로 분리 가능
PLAN = {
    "임신·출산": [{"task": "산모수첩 발급", "when": "D-200"}, {"task": "정부 임신·출산 지원 신청", "when": "D-180"},
                {"task": "출산용품 준비", "when": "D-60"}, {"task": "출생신고 서류 확인", "when": "D-7"}],
    "재난 대비": [{"task": "비상용품 키트 구성", "when": "상시"}, {"task": "대피경로 확인", "when": "상시"},
                {"task": "가족 연락계획 수립", "when": "상시"}, {"task": "취약계층 점검", "when": "상시"}],
}

def _key():
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    if not k:
        try:
            k = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            k = ""
    return k

def generate(topic):
    base = PLAN.get(topic, [])
    key = _key()
    if not key:
        return base  # mock
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        prompt = ("<instructions>상황에 맞는 준비 항목과 시점을 JSON 배열로(중요도순, 누락 없이). "
                  "data 밖은 지어내지 말 것.</instructions>\n"
                  f"<context>{topic}</context>\n<data>{json.dumps(base, ensure_ascii=False)}</data>\n"
                  'JSON: [{"task","when"}]')
        m = c.messages.create(model=MODEL, max_tokens=800, messages=[{"role": "user", "content": prompt}])
        t = m.content[0].text
        return json.loads(t[t.find("["): t.rfind("]") + 1])
    except Exception as e:
        st.warning(f"LLM 실패 → mock: {e}")
        return base

st.title("🗂️ 준비 체크리스트 (데모)")
st.caption("상황을 고르면 시점별 준비 항목을 체크리스트로 만들어 드립니다.")

topics = list(PLAN)
st.session_state.topic = st.selectbox("상황", topics, index=topics.index(st.session_state.topic))
if st.button("체크리스트 생성", type="primary"):
    with st.status("항목 도출 중…") as s:
        st.session_state.items = generate(st.session_state.topic)
        st.session_state.checked = {}
        s.update(label="완료", state="complete")

items = st.session_state.items or PLAN[st.session_state.topic]
st.subheader("체크리스트")
for i, it in enumerate(items):
    key = f"{st.session_state.topic}_{i}"
    st.session_state.checked[key] = st.checkbox(f"**{it['task']}** · {it.get('when', '')}",
                                                value=st.session_state.checked.get(key, False))

done = sum(st.session_state.checked.get(f"{st.session_state.topic}_{i}", False) for i in range(len(items)))
st.progress(done / len(items), text=f"{done}/{len(items)} 완료")
md = "\n".join(
    f"- [{'x' if st.session_state.checked.get(f'{st.session_state.topic}_{i}') else ' '}] {it['task']} ({it.get('when', '')})"
    for i, it in enumerate(items))
st.download_button("체크리스트 다운로드(.md)", f"# {st.session_state.topic} 준비\n{md}\n", "checklist.md")
st.info("다음 행동: 가장 가까운 시점 항목부터 처리하세요.")
