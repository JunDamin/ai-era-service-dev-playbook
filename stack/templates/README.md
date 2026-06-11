# stack/templates — 유형별 보일러플레이트 (clone-and-go)

> **서비스는 결국 유형이 정해져 있다.** 유형을 골라 출발하면 된다.
> 모두 **단일파일·mock으로 즉시 실행**(API 키 불필요), 기본 테마(`../../.streamlit/config.toml`) 자동 적용.
> ※ 템플릿은 **스택의 구현체일 뿐** — 메커니즘의 진실원천은 `../../patterns/*.md`(프레임워크 무관 산문). **기본 출발점은 `fasthtml_app.py`**(기본 스택), Streamlit A~D는 유형별 메커니즘 레퍼런스이자 최소 코드 대안(→ `../fast-prototyping.md` §0). **템플릿 부재 ≠ 금지.**

| 유형 | 파일 | 무엇을 |
|---|---|---|
| **A 추천/매칭** | `recommend_app.py` | 조건 → 받을 수 있는 것 추천 + 신청 연결 |
| **B 의사결정/위험** | `decision_app.py` | 상황 → 위험도·우선순위·행동계획 |
| **C 체크리스트/준비** | `checklist_app.py` | 상황 → 준비 항목·타임라인 체크리스트 |
| **D 문서 생성** | `document_app.py` | 사실 → 민원/신청서/보고서 초안 |
| **★ 위저드 (기본 스택)** | `fasthtml_app.py` | **FastHTML 멀티페이지** — 기본 출발점. 라우트=페이지·세션 누적·confirm·tokens.css·LLM mock. A~D 메커니즘(patterns/*.md)을 이 골격에 얹는다 |

```bash
pip install python-fasthtml && python stack/templates/fasthtml_app.py   # ★ 기본 출발점
streamlit run stack/templates/decision_app.py        # 대안: Streamlit 유형 템플릿 (예: B)
```

- 대부분의 서비스 = **2개 조합**(예: A 추천 + D 문서). 유형 정의·조합은 `../../patterns/`.
- 공통 기본값(빈화면 금지·선택>입력·로딩 표시·복사/다운로드·다음 행동)은 모든 템플릿에 내장(Defaults-first).
- **LLM 연결**은 `recommend_app.py`의 `recommend()` 패턴 참고(B/C/D는 mock 우선 → 같은 방식으로 교체).
