---
name: planning-interview
description: 새 앱·서비스 기획을 시작할 때 사용. "새 앱 기획 시작", "아이디어가 있는데", "이런 서비스 만들고 싶어", "기획 인터뷰" 등에서 호출. 질문을 하나씩 던져 함께 기획하고 기획서(PROJECT.md)를 채운다. 바로 코딩하자는 요청이어도 기획이 없으면 이 스킬부터.
---

# planning-interview — 함께 기획 인터뷰

> 진실원천: `playbook/01-planning-interview.md`(질문 목록·진행 규칙) + `playbook/02-project-template.md`(채울 템플릿). **이 두 파일을 먼저 읽고 그대로 진행하라.**

## 진행 (요약)
1. `playbook/01-planning-interview.md`의 질문 1~10을 **하나씩**, 각 질문에 **추천답을 먼저 제시**하며 진행한다.
   - ★질문 6(UX 철학 — 도착 상태·첫 10초·단순함의 대가)을 건너뛰지 말 것.
2. 답이 모일 때마다 `playbook/02-project-template.md` 사본(`PROJECT.md`)의 해당 칸을 채워 보여준다.
3. 범위가 커지면 "non-goals(v2)로 둘까요?"로 막는다. §1 문제 칸에는 **분석만**(솔루션 금지 — 솔루션은 §5 이후).
4. §1~10 승인 후 §11(개발 지시서)을 생성하고, 문제를 `patterns/README.md`의 모듈(A/B/C/D)에 매핑해 빌드로 넘어간다.

## 빌드로 넘어가기 전 체크
- [ ] **해피패스 유저저니·스토리보드 5칸**(§5b)을 정리했다 — 사람↔AI 공용 기준(정렬·검증·발표·데모 겸용). 와이어프레임/IA/플로우차트는 안 그림.
- [ ] 성공 기준(pass/fail) 1개가 §10에 있다 → `claude-craft/verification-loop.md`
- [ ] 스택 기본값에서 벗어나면 §11에 이유 한 문장 → `stack/fast-prototyping.md` §0
- [ ] `lessons/README.md` 항상-적용 체크리스트를 읽었다
