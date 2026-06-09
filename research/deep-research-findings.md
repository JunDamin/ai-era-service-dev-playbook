# 딥리서치: Claude 기반 AI 앱을 수 시간 내에 빠르게 만드는 법

> 다중 출처 수집 → 적대적 검증 결과. **26개 출처 → 128개 주장 추출 → 25개 3표 검증(전부 확정, 0개 기각).**
> 거의 전부 **Anthropic 1차 출처**. (조사일: 2026-06)

## 핵심 요약 (5개 원칙)
1. **CLAUDE.md는 얇게** + **검증 루프를 닫아라**(pass/fail까지 반복) + **서브에이전트로 컨텍스트 보호**
2. **컨텍스트·도구를 설계하라** — 시스템프롬프트 '적정 고도', 가장 단순한 해법부터, 도구는 적고·고임팩트·비중복, 자율성은 가드레일로
3. **구조화 프롬프트** — 내용유형별 XML 태그, 3~5개 다양·관련·구조화 few-shot
4. **장시간 빌드 하네스** — 요구사항 파일=기준점, 브라우저로 사람처럼 end-to-end 검증, git+진행파일 연속성
5. **AI 슬롭 방지** — UX/ACI에 프롬프트만큼 공들이기

---

## 검증된 발견 (각 항목 신뢰도·출처 포함)

### A. Claude Code 실전

**1) CLAUDE.md는 얇고 고신호로** · 신뢰도 高
- 매 세션 로드됨 → 비대하면 진짜 지시를 무시. **<200줄** 목표.
- 각 줄 점검: "빼면 실수하나? 아니면 삭제." 구체·검증가능("2-space 들여쓰기"). 헤더·불릿 구조화.
- 출처: best-practices, memory

**2) CLAUDE.md 포함/제외** · 高
- 포함: 추측 불가 bash명령, 비표준 코드스타일, 아키텍처 결정, 레포 관례, env 특이사항, 비자명 함정
- 제외: 코드서 추론 가능한 것, 표준 관례, 상세 API문서(링크로), 자주 바뀌는 정보, 긴 튜토리얼, 파일별 설명
- 다단계 절차/한 영역 맥락 → skill·경로스코프 규칙으로
- 출처: best-practices, memory

**3) 검증 루프를 닫아라** · 高
- Claude는 "돼 보이면" 멈춤. pass/fail 체크(테스트·빌드·린트·출력diff·스크린샷)를 주면 통과까지 자율 반복.
- 출처: best-practices

**4) 서브에이전트로 컨텍스트 보호** · 高
- 별도 컨텍스트에서 돌고 요약만 보고 → 조사·검증·**적대적 리뷰**(fresh 컨텍스트)에 사용. `.claude/agents/`에 도구·모델 지정.
- 출처: best-practices

**5) Explore → Plan → Implement → Commit** · 高
- plan mode로 조사/실행 분리. "diff를 한 문장으로 말할 수 있으면 plan 생략." 불확실·다파일·낯선 코드일 때 plan.
- 출처: best-practices

### B. 에이전트·컨텍스트·하네스 엔지니어링

**6) 컨텍스트 엔지니어링 ≠ 프롬프트 엔지니어링** · 高
- 컨텍스트 엔지니어링 = 매 추론마다 **최적 토큰 집합을 큐레이션·유지**(시스템지시·도구·MCP·외부데이터·메시지이력 전체 상태 관리).
- 출처: effective-context-engineering-for-ai-agents

**7) 시스템 프롬프트는 '적정 고도'(Goldilocks)** · 高
- 브리틀한 if-else도, 모호한 고차원 지침도 아닌 중간. 섹션화(`<background_information>`,`<instructions>`, Tool guidance, Output) + **기대행동을 온전히 그리는 최소 정보**.
- 출처: effective-context-engineering-for-ai-agents

**8) 도구 설계에 공들여라(ACI)** · 高
- 도구는 **비중복·자족·견고·매우 명확**. 엔드포인트를 얇게 감싸지 말고 **소수의 고임팩트 도구로 통합**(list_users/list_events/create_event → schedule_event 하나). 도구 많다고 좋아지지 않음. *프롬프트만큼 도구에 투자*.
- 출처: writing-tools-for-agents, effective-context-engineering, building-effective-agents

**9) 도구는 타깃 결과만 반환** · 高
- 전체 데이터셋 나열 ❌(컨텍스트 제약). `list_contacts`보다 `search_contacts`/`message_contact`. 관련성 > 유연성.
- 출처: writing-tools-for-agents

**10) 에이전트를 기본값으로 쓰지 말 것 — 자율성 제어** · 高
- 가장 단순한 해법(단순 프롬프트+평가)부터, 모자랄 때만 다단계 에이전트 추가. 워크플로(정해진 코드경로) vs 에이전트(스스로 경로 결정) 구분. 자율성↑ = 비용·오류↑ → 샌드박스·가드레일로 테스트.
- 출처: building-effective-agents

**11) 장시간 빌드 하네스 패턴** · 高
- 초기화 에이전트가 **요구사항 파일**(전 기능 'failing'으로)을 먼저 작성 → ground truth, 조기 완료 선언 방지.
- **브라우저 자동화로 사람처럼 end-to-end 검증**(단위테스트·curl로는 '실제 작동'을 못 잡음).
- **git 커밋(서술적 메시지) + 진행 파일**로 세션 간 연속성(새 세션은 기억 0).
- 출처: effective-harnesses-for-long-running-agents

### C. 프롬프트 패턴

**12) XML 태그로 구조화** · 高
- 내용유형별 태그(`<instructions>`,`<context>`,`<input>`)로 오해↓. 일관·서술적 태그명, 자연 계층은 네스팅(`<documents>`>`<document index="n">`).
- 출처: use-xml-tags

**13) few-shot 3~5개** · 高
- 출력 형식·톤·구조를 가장 신뢰성 있게 조향. **관련·다양(엣지케이스)·구조화**(`<example>`/`<examples>`). Claude에게 예시 생성/평가도 시킬 수 있음.
- 출처: multishot-prompting

### D. 리포 구조 (종합 도출) · 신뢰도 中(편집적 합성, 개별 팁은 高)
- `claude-craft/`(claude-md·verification-loop·subagents·workflow), `method/`(context-engineering·agents-vs-workflows·tool-design·long-running-harness), `prompts/`(system-prompt-altitude·xml-structure·few-shot), `design/`(anti-slop-ux), `stack/`(fast-prototyping). 각 파일 = 실행팁 + 출처URL + 스니펫.

---

## 주의/갭 (리서치가 명시)
- **스택(Streamlit 단일파일)·디자인 구체(타이포 스케일·컴포넌트 토큰·로딩UX)**는 검증된 1차 주장으론 **원칙만** 확보 — 구체 레시피는 출처 보강 필요.
- 리포 구조는 **편집적 합성(中)**. 디렉터리명은 제안일 뿐.
- 일부 docs URL은 platform.claude.com으로 301 리다이렉트(내용은 최신).
- **<200줄은 소프트 타깃**(길이와 무관하게 전부 로드되지만 길수록 준수율↓).
- end-to-end 검증은 원문이 "대체로 잘함"으로 다소 경험적·웹앱 맥락.

## 미해결 질문 (보강 리서치 후보)
1. Streamlit 단일파일 vs 대안 스택의 구체 권장·함정?
2. 권위 있는 anti-AI-slop 디자인 구체(타이포 스케일·위계·컴포넌트·로딩UX·TTFV)?
3. UI 앱의 검증 루프를 구체적으로 어떻게 배선(스크린샷 diff·Playwright)?
4. 멀티시간 빌드에서 슬래시커맨드 vs 서브에이전트 조합 패턴?

---

## 전체 출처 (품질)
**1차(Anthropic)**
- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/memory
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.anthropic.com/research/building-effective-agents
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts
- https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md

**1차(스택)**
- https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps
- https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
- https://github.com/festiva1300/streamlit-claude-chat
- https://clickhouse.com/docs/use-cases/AI/MCP/ai-agent-libraries/streamlit-agent

**참고(블로그/타사)**
- https://blog.sshh.io/p/how-i-use-every-claude-code-feature
- https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4
- https://gendesigns.ai/blog/ai-generated-ui-mistakes-how-to-fix
- https://alexlavaee.me/blog/lessons-learned-designing-with-ai/
- https://medium.com/@adesemoyeileri/typography-hierarchy-in-ui-ux-design-b4913d60e4fb
- https://github.com/sindresorhus/awesome/blob/main/awesome.md
- https://github.com/trussworks/research-design-playbook
- https://docs.gitlab.com/development/documentation/site_architecture/folder_structure/
