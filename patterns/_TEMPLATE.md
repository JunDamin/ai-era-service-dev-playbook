# <모듈명> (Type X)

> **한 줄:** 이 모듈이 만들어내는 것(=산출물)을 한 문장으로.

## 언제 쓰나
- (이 모듈이 맞는 문제 유형 1~2개)

## 입력 계약 (Input)
- 필요한 **최소** 입력 — 가능하면 선택형(Click·Multi-select). 한 번 받으면 `session_state` 저장.

## 처리 (파이프라인 내 역할)
- 척추(Input→Context→Discovery→Recommendation→Explanation→Action→Artifact) 중
  **이 모듈이 담당하는 단계**와 핵심 로직.

## 산출물 (Artifact)
- Card / Checklist / Timeline / Report / PDF 중 무엇을, 어떤 필드로.

## 조합 예시
- 다른 모듈과 어떻게 합쳐지나 (예: A 추천 + D 문서생성).

## Claude 프롬프트 (복붙)
```
<instructions> … 역할·제약·금지(지어내지 말 것, 자격 판정 금지) … </instructions>
<input>{{...}}</input>
<data>{{고정 데이터}}</data>
출력(JSON 스키마): { … }
```

## 데이터
- 어떤 고정 데이터가 필요한가 → `data-patterns/…`

## 근거 / 출처
- 관련 Rule(CLAUDE.md) · 참고 문서 URL
