# patterns — 조합 가능한 기능 모듈

> **서비스 유형 = 모듈.** 문제 = 척추(Input → Context → Discovery → Recommendation → Explanation → Action → Artifact)에 모듈 **1~N개를 조합**. 대부분 2개 조합.

| 유형 | 정의 문서 | 보일러플레이트 |
|---|---|---|
| **A 추천/매칭** | `recommendation.md` | `../stack/templates/recommend_app.py` |
| **B 의사결정/위험** | `decision.md` | `../stack/templates/decision_app.py` |
| **C 체크리스트/준비** | `checklist.md` | `../stack/templates/checklist_app.py` |
| **D 문서 생성** | `document.md` | `../stack/templates/document_app.py` |

- 조합 예: 혜택 찾기 = **A + D** · 임산부 원스톱 = **C + A** · 재난 가이드 = **B + C** · 생활 불편 = **A + D**
- 새 모듈은 `_TEMPLATE.md` 복제(입력계약→처리→산출물→조합→프롬프트→데이터→근거).
