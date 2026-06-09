# 00 · 전체 개요 (사람과 AI가 같이 보는 법)

> **철학:** AI에게 "코딩해줘"라고 말하기 전에, **AI가 실패하지 않을 환경을 먼저 설계한다.**
> 이 플레이북은 *기획*과 *AI 코딩*을 한 흐름으로 잇고, 사람과 AI가 **같은 문서**를 보며 협업한다.

## 누가 무엇을 보나
| | 사람(기획자/리뷰어) | AI(Claude) |
|---|---|---|
| `01_planning_interview` | 질문에 답하며 생각 정리 | 질문을 던지고 답을 템플릿에 채움 |
| `10_project_template` | 기획서로 검토·승인 | 빌드의 ground truth로 사용 |
| `lessons/` | 원칙 학습·체크 | UI/UX 만들 때 기본값으로 강제 적용 |
| `claude-craft/` | 작업 방식 이해 | 검증 루프·서브에이전트·워크플로 실행 |

## 전체 흐름
```
아이디어
 1) 함께 기획   → 01_planning_interview (AI가 질문 → 사람이 답 → 함께 좁힘)
 2) 기획 확정   → 10_project_template 채움 (1~10 = 기획, 11 = 개발 지시서)
 3) 하네스 깔기 → requirements.md(전부 failing) + non-goals + 보일러플레이트
 4) 병렬 빌드   → 서브에이전트/2인 분업 + lessons 기본값 적용
 5) 검증        → 성공 기준(pass/fail) 통과까지 end-to-end 반복
 6) 마무리      → 작동 데모 + 발표
```

## 4기둥 (자세히)

### ① 함께 기획 (상호작용)
- 바로 코딩 금지. **질문을 하나씩** 던져(추천답 제시) 문제·대상·핵심 가치·비목표·성공 기준을 좁힌다.
- → `01_planning_interview.md`

### ② 하네스 먼저 (문제가 커지지 않게)
- **요구사항 파일**을 먼저 써 기준점으로(조기 완료·무한 확장 방지).
- **non-goals**(로그인·권한·다국어·결제…)를 박아 스코프 크리프 차단. → `lessons/MVP.md`
- **보일러플레이트**(단일파일 스택)로 시작 비용 0에 가깝게. → `stack/` (예정)
- → `claude-craft/workflow.md`, `research/deep-research-findings.md`

### ③ 병렬로 빠르게
- 독립 작업은 동시에: **2인 분업**(A=빌드 드라이빙 / B=데이터·정확성·발표) + **서브에이전트**(조사·정확성 리뷰를 별도 컨텍스트로).
- → `claude-craft/subagents.md`

### ④ 실패하지 않을 환경
- 코딩 전에 **검증 기준(pass/fail)**과 **UX 기본값**(lessons 체크리스트)을 먼저 설계.
- → `lessons/README.md`, `claude-craft/verification-loop.md`

## 4시간 타임박스 (해커톤)
0–30 기획 인터뷰+템플릿 / 30–60 하네스(요구사항·non-goals·보일러플레이트) / 60–180 병렬 빌드(검증 ON) / 180–210 polish / 210–240 발표. → `claude-craft/workflow.md`
