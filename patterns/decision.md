# 의사결정 (Decision, Type B)

> **한 줄:** 상황을 받아 위험도·우선순위를 판단하고 **행동 계획**으로 연결한다.

## 언제 쓰나
- 재난 대응, 위험도 분석, "지금 어떻게 해야 하나"류

## 입력 계약
- 선택형 우선: 지역 · 상황 유형 · 조건(예: 가족 구성). 받은 값은 `session_state` 저장.

## 처리 (파이프라인 내 역할)
- Context Extraction: 입력 → 상황 프로필
- 위험 평가: 고정 규칙/데이터 기반 위험도 산정(코드) + LLM 설명
- 우선순위 + 행동 계획 도출

## 산출물 (Artifact)
- **위험도(시그널 색)** · 우선순위 · **행동 계획 카드**(지금 할 일 순서)
- 조합: **+ Type C**(체크리스트) → 준비 항목까지

## Claude 프롬프트 (복붙)
```
<instructions>
상황으로 위험도(High/Med/Low)와 우선순위, 즉시 행동을 제시.
- 단정적 '판정'(의료·법률) 금지. 불확실하면 confidence='확인 필요'.
- data 밖은 지어내지 말 것.
</instructions>
<situation>{{profile}}</situation>
<rules_or_data>{{fixed_data}}</rules_or_data>
출력(JSON): [{ "risk","priority","action","why","confidence","source_url" }]
```

## 데이터
- `data-patterns/` 위험/행동요령 고정 데이터(예: 재난 행동요령)

## 근거 / 출처
- 행동>정보·결과물 = CLAUDE.md Rule 1·4 · 시그널/위계 = `lessons/dashboard.md`
