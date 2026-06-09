# method/tool-design — 도구 · ACI 설계

> 근거: Anthropic(1차).

## 원칙
- 도구는 **적고 · 비중복 · 자족 · 매우 명확**. 사람도 못 고를 도구면 모델도 못 고른다.
- 엔드포인트를 얇게 감싸지 말고 **고임팩트로 통합**(list_users/list_events/create_event → `schedule_event` 하나).
- 결과는 **타깃만 반환**(전체 데이터셋 나열 금지) — 컨텍스트 절약(`search_*` > `list_*`).
- **ACI(도구 인터페이스)에 프롬프트만큼 투자.**

## 4시간 적용
- 데이터 조회 도구는 "조건에 맞는 후보만" 반환하도록.

## 출처
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://www.anthropic.com/research/building-effective-agents
