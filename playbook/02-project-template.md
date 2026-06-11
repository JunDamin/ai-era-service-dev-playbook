# 새 앱 기획 템플릿 (Idea → 기획서 초안 → 개발 지시서)

> **철학:** AI에게 "코딩해줘"라고 말하기 전에, **AI가 실패하지 않을 환경을 먼저 설계한다.**
> 사용법: 이 파일을 복제해 아이디어를 채운다 → 1~10은 *기획*, 11은 *AI 개발 지시서*. Claude에게 통째로 주고 빌드 시작.

---

## 1. Problem (문제)
- 무엇이 문제인가? (한 문장)
> 

## 2. Target User (대상)
- **누구의** 문제인가? 구체적 1인 페르소나(이름·상황).
> 

## 3. Current Workflow (현재 흐름)
- 지금은 이 일을 어떻게 하나? 어디서 시간을 쓰나?
> 

## 4. Pain Point (막히는 지점)
- 현재 흐름에서 **어디서 막히고 포기하나?** (가장 아픈 1개)
> 

## 5. Core Value (가장 작은 가치 단위) + 서비스 철학
- "이 앱은 **[대상]**이 **[과업]**을 **[결과물]**로 끝내게 한다." → `lessons/mvp.md`
> 
- **서비스 철학 (UX의 헌법 — 화면·문구·입력이 전부 여기서 나온다):**
  - 도착 상태: 사용자는 **[어떤 감정·상황]**으로 온다.
  - 첫 10초: **[무엇 하나]**만 이해시킨다. (한 화면 한 목표 → `lessons/input-patterns.md` P4)
  - 단순함의 대가: 그러기 위해 **[무엇]**을 숨기거나 대신해 준다.
> 

## 6. MVP Scope (범위)
- **만들 것(최소):**
- **절대 안 만들 것(non-goals):** (로그인·권한·다국어·결제 기본 제외) → `lessons/mvp.md`
> 

## 7. Input / Output (입력·출력)
- **입력:** (선택>입력 — 드롭다운/칩/피커 우선) → `lessons/data-input.md`
- **출력(결과물):** Card/Checklist/Timeline/Report/PDF 중 무엇 → `patterns/`
> 

## 8. UX Requirements (UX 요건)
- 적용할 기본값(항상): `lessons/README.md` 체크리스트
  - [ ] 빈 화면 금지(예시·스켈레톤)  [ ] 영구 레이블  [ ] on-blur 검증
  - [ ] 좋은 기본값·설정 최소화  [ ] 복사/다운로드  [ ] 다음 행동 안내  [ ] 위계(강조 소수)
> 

## 9. Failure Cases (실패 시나리오)
- 사용자가 어디서 막힐까? 잘못 입력하면? 데이터 없으면? AI가 틀리면?
- 각각의 대비(빈/오류/로딩 상태) → `lessons/ux.md`, `lessons/ai-chat.md`
> 

## 10. Validation Criteria (성공 기준 = pass/fail)
- "○○ 시나리오를 사용자가 끝까지 완료" 같은 **검증 가능한 1개** → `claude-craft/verification-loop.md`
> 

---

## 11. AI Coding Instructions (개발 지시서)
> Claude에게 줄 빌드 규칙. 위 1~10을 근거로 아래를 **강제**한다.

- **스택:** 기본값 = **FastHTML 단일 파일**(+`design/tokens.css`, 빌드 전 llms-ctx 하네스) → `stack/templates/fasthtml_app.py`
  - 기본값에서 벗어나면 **이유 한 문장**: > _(예: "내부 검증용 최소 폼이라 Streamlit" / "LLM 불요 정적 배포라 HTML 단일 파일")_ → 선택 기준 `stack/fast-prototyping.md` §0
- **요구사항 파일 먼저:** 기능 목록을 `requirements.md`로 작성(전부 'failing') → 기준점 → `claude-craft/workflow.md`
- **반드시 포함:**
  - 샘플/고정 데이터 포함(실시간 API 의존 X) → `data-patterns/`
  - 빈 화면 금지(예시 프리필) · 복사/다운로드 버튼 · 친절한 오류 메시지(필드 옆)
  - 좋은 기본값 · 로딩은 진행/스트리밍 표시
  - 추천엔 Confidence + 출처, 자격 '판정'은 하지 말 것
- **검증:** 10번 기준을 **브라우저로 사람처럼 end-to-end** 통과까지 반복 → `claude-craft/verification-loop.md`
- **커밋:** 단계마다 git 커밋 + 진행 요약(세션 연속성)

> 완료 정의: **10번 Validation 통과 + 8번 체크리스트 충족.**
