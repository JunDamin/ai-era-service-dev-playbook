# method/spec-first — 스펙 주도 개발 (AI와 함께 기획)

> 근거: GitHub Spec Kit(1차) — 3차 리서치 검증.

## 원칙
- 코드가 아니라 **스펙(의도)이 진실 원천**. 스펙 = "코드가 어떻게 동작해야 하는가"의 계약.
- 4단계(좌→우 의존): **/specify**(무엇·왜) → **/plan**(설계) → **/tasks**(분해) → **/implement**(구현).

## 플레이북 연결
- 우리 흐름의 **'요구사항 파일'이 곧 spec**.
- `playbook/01_planning_interview`로 spec을 뽑고, `playbook/10_project_template`이 그 계약서, `claude-craft/long-running-harness`의 requirements.md가 실행용 spec.

## 4시간 적용
- 0–30분에 **spec(요구사항)부터 확정** → 그 위에서만 구현. 모호하면 인터뷰로 좁힘.

## 출처
- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://github.com/github/spec-kit
