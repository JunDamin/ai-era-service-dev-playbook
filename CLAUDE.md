# 인공지능 시대의 서비스 개발 플레이북 — 운영 지침

**사람과 AI가 같이 보는 플레이북.** 아이디어를 *검토 가능한 기획*으로 만들고, AI 코딩의 시행착오를 줄여 **짧은 시간에** 작동하는 서비스를 만든다.
Claude는 이 파일을 운영체제로 삼는다. (전체 안내: `playbook/00-overview.md`)

## 4기둥
- **함께 기획(상호작용):** 바로 코딩하지 말고, 사용자와 **기획 인터뷰**로 문제·범위를 먼저 좁힌다(질문 하나씩, 추천답 제시). → `playbook/01-planning-interview.md`
- **하네스 먼저(문제 억제):** 요구사항 파일·non-goals·보일러플레이트를 먼저 깔아 *문제가 커지지 않게* 한다. → `claude-craft/`
- **병렬로 빠르게:** 독립 작업은 서브에이전트/2인 분업으로 동시에. → `claude-craft/subagents.md`
- **실패하지 않을 환경:** "코딩해줘" 전에 검증 기준·UX 기본값을 먼저 설계. → `lessons/`, `claude-craft/verification-loop.md`

## 5대 Rule (항상 적용)
1. 정보가 아니라 **행동**을 제공한다. ("대상입니다" ❌ → "지금 ○○를 신청하세요 / 서류는 … / 예상 20분" ✅)
2. 입력보다 **선택**을 우선한다. (Click > Multi-select > Short text > 자연어)
3. 한 번 받은 정보는 **다시 묻지 않는다**. 세션에 저장, 수정만 허용.
4. 모든 추천은 **결과물을 생성한다**. (체크리스트·PDF·행동계획·민원초안 중 1개 이상)
5. 새 정보를 만들지 말고 기존 정보를 **압축·우선순위화·행동화**한다.

## 기본값 우선 (Defaults-first) ★
좋은 기본값(디자인 토큰·UX 동작·스택 설정·모듈)을 **미리 박아둬, 일정 수준까지는 결정 없이 작동**하게 한다.
- **문제 고유한 것만 정한다.** 나머지는 기본값을 상속 → **필요할 때만 override.**
- 색·간격·타이포·로딩·에러·복사/다운로드·confidence는 *물어보지 않고* 기본 적용.
- 구현 위치: `design/`(토큰·테마) · `stack/templates/recommend_app.py`(동작 기본값) · `lessons/defaults.md`(원칙)

## 빌드 파이프라인 (척추)
Input → Context Extraction → Candidate Discovery → Recommendation → Explanation → Action Planning → Artifact Generation

## 문제 → 모듈 조합
문제를 받으면: (a) 파이프라인에 매핑 → (b) 아래 모듈을 1~N개 골라 조합 → (c) **좁은 1개 시나리오부터 완주**.
- 추천형(A) · 의사결정형(B) · 체크리스트형(C) · 문서생성형(D) → `patterns/`(README + 각 모듈) 참조
- 대부분의 문제 = 2개 조합 (예: 혜택 추천 A + 신청가이드 D)

## 기본 스택 (세팅 최소)
- **Streamlit 단일 파일 + `st.session_state` + LLM 직접 호출.** 무거운 프레임워크(LangGraph 등) 금지.
- **출발점: `stack/templates/recommend_app.py`** (clone 즉시 실행되는 보일러플레이트) — 이 위에 빌드.

## 출력 계약
- 모든 화면은 **10초 안에 가치**를 보여준다. 로딩 중엔 "이해한 상황 / 발견한 후보"를 표시(빈 스피너 ❌).
- 추천엔 **Confidence**(확정/높음/중간/확인 필요) 라벨. 불확실하면 **출처 링크 병기**.
- 결과는 반드시 **Artifact**(Card/Checklist/Timeline/Report/PDF) 하나로 끝맺는다.

## 작업 방식
- **Explore → Plan → Implement → Commit.** diff를 한 문장으로 말할 수 있으면 plan 생략. → `claude-craft/workflow.md`
- **검증 루프**: 완료 기준(pass/fail)을 먼저 정하고 통과할 때까지 반복. UI는 브라우저로 사람처럼 end-to-end 확인. → `claude-craft/verification-loop.md`
- 조사·정확성 리뷰는 **서브에이전트**(별도 컨텍스트)로. → `claude-craft/subagents.md`

## 데이터 원칙
- **실시간 API 의존 금지.** 미리 큐레이션한 **고정 데이터** 사용(`data-patterns/`). 항상 공식 출처 링크 병기.
- AI는 자격 **'판정'을 하지 않는다**(확인 필요로 표시). 단순 조회·계산은 코드로.

## 라우팅 (필요할 때만 읽기)
- **새 앱 시작 → `playbook/01-planning-interview.md`(함께 기획) → `playbook/02-project-template.md`(채움)**
- **데모/발표 → `playbook/03-demo.md`** (검증 시나리오를 'S-tier 피치'로 — 빌드만큼 점수)
- **UI/UX → `lessons/README.md` 체크리스트 항상 적용** (+ lessons/ux·data-input·defaults·dashboard·ai-chat·mvp)
- **디자인(색·간격·타이포) → `design/design-tokens.md`(기본값)·`design/design-system.md`** · **UI 마감 → `design-polish` 스킬**(동봉, `.claude/skills/`) · 스킬 안내 → `claude-craft/skills-setup.md`
- **스택·빌드 → `stack/templates/recommend_app.py`·`stack/fast-prototyping.md`** · **데이터 → `data-patterns/`**
- **엔지니어링 → `method/`**(context-engineering·tool-design·long-running-harness·agents-vs-workflows·spec-first)
- **프롬프트 → `prompts/`** · **Claude Code 실전 → `claude-craft/`** · **근거 → `research/`**

## 금지
- 200줄 넘는 CLAUDE.md · 사전 완성된 정답 코드 · 실시간 API 가정 · 행동 없는 정보 나열
