# 체크리스트 (Checklist, Type C)

> **한 줄:** 목표·상황을 받아 **준비물·일정·행동 체크리스트**를 생성한다.

## 언제 쓰나
- 출산 준비, 재난 대비, 절차 준비 등 "무엇을 언제 준비하나"류

## 입력 계약
- 선택형 우선: 상황 · 시점(예: 출산 예정일·D-day) · 조건. `session_state` 저장.

## 처리 (파이프라인 내 역할)
- Context → 필요한 단계/항목 도출(고정 데이터+LLM) → 시점별 정렬

## 산출물 (Artifact)
- **체크리스트(완료 토글)** + **타임라인** + 다운로드(.md)
- 조합: **+ A**(추천 항목) · **+ D**(신청 문서)

## Claude 프롬프트 (복붙)
```
<instructions>
상황에 맞는 준비 항목과 시점을 체크리스트로. 누락 없이, 중요도순.
- data 밖은 지어내지 말 것. 불확실하면 '확인 필요'.
</instructions>
<context>{{profile}}</context>
<items_or_data>{{fixed_data}}</items_or_data>
출력(JSON): [{ "task","when","why","done":false,"source_url" }]
```

## 데이터
- `data-patterns/` 단계·항목 고정 데이터

## 근거 / 출처
- 한 화면 한 과제·스캔성 = `lessons/UX.md` · 결과물 다운로드 = `lessons/Dashboard.md`
