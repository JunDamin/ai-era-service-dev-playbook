# AGENTS.md — AI 코딩 에이전트 운영 지침

> 이 리포는 **"인공지능 시대의 서비스 개발 플레이북"** — 아이디어를 검토 가능한 기획으로 만들고, 짧은 시간(수 시간)에 작동하는 서비스를 만들기 위한 운영 문서다.
> 어떤 에이전트든 이 파일이 진입점이다. (Claude Code는 `CLAUDE.md`를 자동 로드 — 내용 동일 취지, 그쪽이 더 상세)

## 무엇을 하는 리포인가
- 코드 모음이 아니라 **사람과 AI가 함께 따르는 방법론**: 기획 인터뷰 → 기획서 → 하네스 → 병렬 빌드 → 검증 → 데모.
- 새 작업 시작: `playbook/01-planning-interview.md`의 질문으로 사용자와 **함께 기획**부터. 바로 코딩하지 말 것.

## 명령어
```bash
pip install -r requirements.txt
python stack/templates/fasthtml_app.py           # 기본 보일러플레이트(키 없어도 mock 동작)
streamlit run stack/templates/recommend_app.py   # 대안: Streamlit A~D 유형 템플릿
```

## 항상 적용 (5대 Rule)
1. 정보가 아니라 **행동**을 제공한다. 2. 입력보다 **선택** 우선. 3. 받은 정보는 **다시 묻지 않는다**(세션 저장).
4. 모든 추천은 **결과물**(체크리스트·문서·다운로드)을 생성한다. 5. 새 정보 생성 말고 기존 정보를 **압축·우선순위화·행동화**.

## 스택
- **기본값: FastHTML 단일 파일** + 세션 + LLM 직접 호출 + `design/tokens.css`. **빌드 전 `https://fastht.ml/docs/llms-ctx.txt` 를 먼저 읽을 것**(환각 방지). 프레임워크는 아이디어 크기에 비례 — 벗어나면 이유 한 문장(Streamlit=최소 코드 검증·HTML=LLM 불요 정적 → `stack/fast-prototyping.md` §0).
- 실시간 API 의존 금지 — 큐레이션한 **고정 데이터**(`data-patterns/`) + 공식 출처 링크. AI는 자격 '판정'을 하지 않는다.

## 구조 (필요할 때만 읽기 — progressive disclosure)
| 경로 | 내용 |
|---|---|
| `playbook/` | 흐름: 01 기획인터뷰 → 02 기획서 템플릿 → 03 데모 |
| `patterns/` | 기능 모듈 A 추천·B 위험·C 체크리스트·D 문서 (+빈칸 비대칭 표) |
| `stack/` | 유형별 보일러플레이트 + 스택 선택 규칙 + Streamlit 함정 |
| `lessons/` | UX 교훈(입력 패턴·라이팅·대시보드·기본값·MVP) — UI 만들 때 강제 적용 |
| `design/` | 디자인 토큰·AI 슬롭 회피 |
| `data-patterns/` | 데이터 수집법·스키마·도그푸딩 교훈 |
| `method/` · `prompts/` · `claude-craft/` | 엔지니어링·프롬프트 패턴·Claude Code 실전 |
| `.claude/skills/` | 동봉 스킬(Claude Code 전용 — 다른 에이전트는 해당 문서를 직접 읽으면 동일) |

## 작업 방식
- Explore → Plan → Implement → Commit. **검증 루프**: 완료 기준(pass/fail)을 먼저 정하고 통과까지 반복 — 로직 먼저 테스트, UI는 브라우저로 end-to-end(→ `claude-craft/verification-loop.md`).
- 금지: 행동 없는 정보 나열 · 실시간 API 가정 · 사전 완성된 정답 코드.
