# 검증 루프 (Verification Loop)

## 원칙
- Claude는 **"돼 보이면" 멈춘다.** 체크가 없으면 'looks done'이 유일한 신호.
- **pass/fail 신호**를 주면 루프가 스스로 닫힌다 — 작업 → 체크 실행 → 결과 읽기 → 통과까지 반복.

## 체크 후보
- 테스트 스위트 / 빌드 exit code / 린트 / 출력 diff(fixture 대비) / **스크린샷 vs 디자인**

## 실천 (해커톤용)
- 빌드 **시작 전 "완료 기준 1개"를 먼저 정의** → Claude에게 "이 체크 통과까지 반복" 지시
- UI 앱이면: **브라우저 자동화로 사람처럼 핵심 시나리오 1개를 끝까지** (코드 단위 테스트·curl만으론 '실제로 작동'을 못 잡음)

## 2단계 검증 — 로직 먼저, 브라우저 나중 (드라이런 3종으로 검증)
- **조건:** Streamlit 등 UI 앱을 만든다면 → **처리 로직(필터·계산·점수·분류)을 UI 없이 먼저 테스트**하고, 통과 후에 브라우저 end-to-end로 간다.
- **전제 구조:** 로직은 **모듈 레벨 함수**, UI는 `main()` + `if __name__ == "__main__":` 가드 → `import app` 후 임시 스크립트(`_t.py`)로 케이스를 돌릴 수 있다.
- **왜:** 브라우저 검증은 느리고(rerun·클릭), 로직 버그와 UI 버그가 섞이면 원인 추적이 2배. 로직을 먼저 통과시키면 브라우저에선 UI 문제만 남는다 — 실측: 3번째 드라이런은 이 순서 덕에 브라우저 버그 0건.
- **순서:** ① 로직 함수 작성 → ② `_t.py`로 대표 케이스+엣지(빈 입력·경계값) 검증 → ③ `streamlit run` + 브라우저로 happy path 1개 완주 → ④ 통과한 시나리오 = 데모 스크립트(`playbook/03-demo.md`).

## 스니펫 (Claude에게 줄 지시문)
> "구현 후 `streamlit run app.py`로 띄우고, '기초연금 신청 완주' 시나리오를
>  네가 직접 클릭해 끝까지 가봐. 막히면 고치고, **완주될 때까지 반복**해."

## 출처
- https://code.claude.com/docs/en/best-practices
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
