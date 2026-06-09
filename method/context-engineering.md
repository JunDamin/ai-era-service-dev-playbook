# method/context-engineering — 컨텍스트 엔지니어링

> 근거: Anthropic(1차).

## 원칙
- 컨텍스트 엔지니어링 = 매 추론마다 **최적 토큰 집합을 큐레이션·유지**(시스템지시·도구·외부데이터·이력 전체 상태). 프롬프트 작성보다 넓은 개념.
- 성능은 "얼마나 넣느냐"가 아니라 "**무엇을 넣느냐**".

## 어떻게
- 필요한 **최소 정보만** 컨텍스트에(잡음 제거). 큐레이션은 매 턴 반복.
- CLAUDE.md 얇게 + 상세는 **on-demand 라우팅**으로 불러오기.

## 4시간 적용
- 문제와 무관한 파일은 안 읽힌다. 라우팅대로 필요한 것만.

## 출처
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
