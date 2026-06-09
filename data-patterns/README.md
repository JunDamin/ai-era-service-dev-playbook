# data-patterns — 고정 데이터

> **원칙: 실시간 API 의존 금지.** 미리 큐레이션한 고정 데이터를 쓴다(속도·안정·정확). 항상 **공식 출처 링크 병기**, AI는 데이터 밖을 지어내지 않음("확인 필요").

## 스키마 (예: welfare_sample.json)
```
name · target · benefit · how_to_apply · documents · source_url · confidence
```
- `confidence`: 확정 / 높음 / 중간 / 확인 필요 (보정된 값일 때만 신뢰 — `lessons/ai-chat`)

## 쓰는 법
- 모듈(`patterns/`)이 이 데이터에서 **자격 후보를 코드로 필터** → LLM은 우선순위·설명·결과물 생성.
- 새 도메인은 같은 스키마로 파일 추가(예: `disaster_sample.json`).

> ⚠️ 샘플 수치는 예시 — 실제 사용 전 공식 출처로 확인.
