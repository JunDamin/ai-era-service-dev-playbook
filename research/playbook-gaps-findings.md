# 딥리서치 3차: 플레이북 갭 채우기 (AI UX·스택·기획·병렬·디자인)

> 26개 출처 → 121개 주장 → 25개 검증(22 확정 / **3 기각**). NN/g·Streamlit·GitHub Spec Kit 등 1차 위주. (조사일: 2026-06)

## 검증된 발견 (高)
1. **신뢰 보정(trust calibration)** — ① 1인칭 불확실성("확실치 않지만…")이 과신을 줄임 ② confidence(High/Med/Low)는 **보정됐을 때만** 유효 ③ 출처는 눈에 띄게. [NN/g hallucinations](https://www.nngroup.com/articles/ai-hallucinations/)
2. **출처 ≠ 검증** — AI 출처는 자주 환각(존재X URL)이고 사용자는 거의 클릭 안 함(~1%). 자신감 있게 보이면 *부당한 신뢰*. → 출처만으로 안심 금지. [NN/g explainable-ai](https://www.nngroup.com/articles/explainable-ai/)
3. **응답시간** — **0.1s=즉각**(피드백 불필요), **10s=주의 한계**(넘으면 진행상태+중단 옵션). [NN/g](https://www.nngroup.com/articles/response-times-3-important-limits/) · ✗*1초 한계는 기각*
4. **스켈레톤 > 빈 화면/스피너** — 와이어프레임형 자리표시로 체감속도↑(10s 이하). [NN/g skeleton](https://www.nngroup.com/articles/skeleton-screens/) · ✗*구체 2s/10s 임계는 기각*
5. **Streamlit 단일파일 챗 <50줄** — `session_state`로 히스토리, `st.write_stream(stream=True)`로 토큰 스트리밍. [docs](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)
6. **캐싱** — `st.cache_data`가 기본(복사본→안전), `st.cache_resource`는 모델·DB연결용(공유→동시성 위험). [docs](https://docs.streamlit.io/develop/concepts/architecture/caching)
7. **시크릿** — 키 코드/커밋 금지, `st.secrets`+`secrets.toml`(gitignore). [docs](https://docs.streamlit.io/develop/concepts/connections/secrets-management)
8. **스펙 주도 개발(Spec-first)** — 스펙이 계약·진실원천. Spec Kit 4단계 `/specify · /plan · /tasks · /implement`. [GitHub blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/), [spec-kit](https://github.com/github/spec-kit)

## ⛔ 기각(사용 금지)
- 1.0초 응답 중간한계 · "<2s 무표시/2-10s 스켈레톤/>10s 진행바" 구체 임계 · "모호 프롬프트가 수천 요구를 추측하게 한다"

## ⚠️ 갭(검증 통과 0 → 실무 출처로 '잠정' 채움)
- **디자인 'AI 슬롭' 회피**(8pt·타이포 스케일·shadcn/Tailwind·위계): [mindstudio](https://www.mindstudio.ai/blog/claude-design-avoid-ai-slop-design-system), [figma](https://www.figma.com/blog/designer-framework-for-better-ai-prompts/), [shadcn/tailwind](https://ctxs.ai/weekly/shadcn-ui-tailwind-v4-7z8p3v) → `design/`
- **병렬 에이전트·바이브코딩 실패패턴**: [Anthropic multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system), [building-effective-agents](https://www.anthropic.com/research/building-effective-agents), [Simon Willison vibe-engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/) → `method/`

## 주의(반드시 동반)
- confidence는 **보정 안 되면 오히려 오도**(LLM 자기보고 신뢰도는 종종 부정확). 
- 출처는 **검증 발판과 함께**(출처만으론 검증행동 안 일어남).
