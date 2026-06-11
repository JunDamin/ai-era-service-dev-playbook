# method — AI 빌드 엔지니어링 (한 파일)

> 근거: Anthropic(1차) · GitHub Spec Kit(1차) · MAST(피어리뷰) · Willison(실무).
> 요약판은 `research/build-principles.md`(7원칙) — 이 파일은 그 원칙들의 **상세·근거**.

## 1. 컨텍스트 엔지니어링
- 매 추론마다 **최적 토큰 집합을 큐레이션**(시스템지시·도구·데이터·이력). 성능은 "얼마나"가 아니라 "**무엇을** 넣느냐".
- CLAUDE.md 얇게 + 상세는 on-demand 라우팅. 문제와 무관한 파일은 안 읽힌다.

## 2. 스펙 먼저 (spec-first)
- 코드가 아니라 **스펙(의도)이 진실 원천**. 4단계: specify(무엇·왜) → plan → tasks → implement.
- 우리 흐름 매핑: `01-planning-interview`로 spec 추출 → `02-project-template`이 계약서 → `requirements.md`(전부 failing)가 실행용 spec.

## 3. 장시간 빌드 하네스
- **요구사항 파일**(전 기능 'failing') = ground truth — 조기 완료 선언·무한 확장을 막는다.
- **end-to-end 검증**(브라우저로 사람처럼) + **git 커밋(서술적)·진행 파일** = 세션 간 연속성(새 세션은 기억 0).
- 4시간: 0–30분 requirements.md → 단계마다 커밋.

## 4. 워크플로 vs 에이전트 — 단순함부터
- **가장 단순한 해법**(프롬프트+평가)부터. **워크플로**=정해진 경로 / **에이전트**=LLM이 경로 결정. 자율성↑=비용·오류↑ → 가드레일 안에서.
- **멀티에이전트 비용:** 단일 챗 대비 ~4x 토큰, 멀티 ~15x. **더 많은 에이전트 ≠ 더 좋음**(MAST: 실패 14모드 — 명세 / 정합 / 검증·종료). 이득은 breadth-first 탐색·리서치뿐, **대부분의 코딩엔 손해**. → 기본은 단일 에이전트.
- 오케스트레이터-워커를 쓸 땐: 서브에이전트마다 **목표·출력형식·도구·경계**를 명시.
- 병렬화(플레이북 ③기둥): 2인 분업(A=빌드/B=데이터·발표) + 조사·리뷰는 서브에이전트(→ `claude-craft/subagents.md`).

## 5. 도구·ACI 설계
- 도구는 **적고·비중복·자족·명확**. 사람도 못 고를 도구면 모델도 못 고른다.
- 엔드포인트 얇은 포장 ❌ → 고임팩트 통합(`schedule_event` 하나). 결과는 **타깃만 반환**(`search_*` > `list_*`) — 컨텍스트 절약.

## 6. 검증 규율 (바이브 엔지니어링)
- '바이브코딩'과 '엔지니어링'을 가르는 건 **검증·책임**. **자동 테스트가 단일 최대 enabler.**
- ⚠️ AI 생성 테스트는 거짓 자신감 위험(의도를 검증해야) · 단위테스트만으론 불충분 → **브라우저/결과 수준 검증**(→ `claude-craft/verification-loop.md`).

## 출처
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/research/building-effective-agents · https://www.anthropic.com/engineering/writing-tools-for-agents
- https://www.anthropic.com/engineering/multi-agent-research-system · https://arxiv.org/abs/2503.13657 (MAST)
- https://github.com/github/spec-kit · https://simonwillison.net/2025/Oct/7/vibe-engineering/
