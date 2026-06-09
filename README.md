# 인공지능 시대의 서비스 개발 플레이북
### Service Development Playbook for the AI Era

> **사람과 AI가 같이 보는** 플레이북.
> 아이디어를 *검토 가능한 기획*으로 만들고, AI 코딩의 시행착오를 줄여 **짧은 시간에** 작동하는 서비스를 만든다.

코드는 AI가 다시 써준다. 재사용할 자산은 **설계 원칙·실패 사례·기획 흐름**이다.
그래서 이 리포는 "코드 모음"이 아니라 **사람과 AI가 함께 읽고 따르는 운영 문서**다.

## Quickstart (clone-and-go) — 중간에서부터 시작
```bash
git clone https://github.com/JunDamin/ai-era-service-dev-playbook && cd ai-era-service-dev-playbook
pip install -r requirements.txt
streamlit run stack/streamlit_template.py     # 보일러플레이트 즉시 실행(키 없어도 mock)
```
그다음 **Claude Code로 이 폴더를 열면** `CLAUDE.md`가 자동 로드 → AI가 플레이북을 이미 안다.
새 작업은 한마디로 시작: **"새 앱 기획 시작"** → AI가 `playbook/01_planning_interview.md`로 질문을 던지며 함께 기획 → `stack/` 보일러플레이트 위에 빌드.

> 즉 clone 한 순간 *설정·보일러플레이트·원칙·검증 기준*이 이미 깔려 있어, **문제만 끼우면 된다.**

## 무엇을 해주나 (4기둥)
1. **함께 기획(상호작용)** — AI가 질문을 던지며 사용자와 문제·범위를 좁힌다.
2. **하네스 먼저(문제 억제)** — 요구사항·non-goals·보일러플레이트를 먼저 깔아 *문제가 커지지 않게*.
3. **병렬로 빠르게** — 독립 작업은 서브에이전트/2인 분업으로 동시에.
4. **실패하지 않을 환경** — 코딩 전 검증 기준·UX 기본값을 먼저 설계.

## 구조
| 폴더/파일 | 역할 | 상태 |
|---|---|---|
| `CLAUDE.md` | 운영 지침(사람·AI 공통 뇌) | ✅ |
| `playbook/00_overview.md` | 전체 사용법·흐름·역할 | ✅ |
| `playbook/01_planning_interview.md` | 함께 기획(질문 인터뷰) | ✅ |
| `playbook/10_project_template.md` | 기획서 초안 → 개발 지시서 템플릿 | ✅ |
| `lessons/` | 설계 교훈(UX·입력·기본값·대시보드·AI·MVP, NN/g 근거) | ✅ |
| `claude-craft/` | Claude Code 실전(클로드MD·검증·서브에이전트·워크플로) | ✅ |
| `patterns/` | 조합 가능한 기능 모듈(추천/의사결정/체크리스트/문서) | ⏳ 추천만 |
| `research/` | 딥리서치 근거(claude-app, ux-design) | ✅ |
| `method/` `prompts/` `design/` `stack/` `data-patterns/` | 심화·스택·데이터 | ⏳ |

## 흐름 (사람 ↔ AI)
```
아이디어
 → [01] 기획 인터뷰 (AI가 질문, 사람이 답 → 함께 좁힘)
 → [10] 템플릿 채움 (기획서 초안)
 → 하네스/보일러플레이트 + non-goals (문제 억제)
 → 병렬 빌드 (서브에이전트/2인) + 검증 루프
 → 작동하는 서비스
```

> 시작점: **`playbook/00_overview.md`** 읽기 → 새 작업은 `playbook/01_planning_interview.md`로.
