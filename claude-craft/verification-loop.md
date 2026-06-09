# 검증 루프 (Verification Loop)

## 원칙
- Claude는 **"돼 보이면" 멈춘다.** 체크가 없으면 'looks done'이 유일한 신호.
- **pass/fail 신호**를 주면 루프가 스스로 닫힌다 — 작업 → 체크 실행 → 결과 읽기 → 통과까지 반복.

## 체크 후보
- 테스트 스위트 / 빌드 exit code / 린트 / 출력 diff(fixture 대비) / **스크린샷 vs 디자인**

## 실천 (해커톤용)
- 빌드 **시작 전 "완료 기준 1개"를 먼저 정의** → Claude에게 "이 체크 통과까지 반복" 지시
- UI 앱이면: **브라우저 자동화로 사람처럼 핵심 시나리오 1개를 끝까지** (코드 단위 테스트·curl만으론 '실제로 작동'을 못 잡음)

## 스니펫 (Claude에게 줄 지시문)
> "구현 후 `streamlit run app.py`로 띄우고, '기초연금 신청 완주' 시나리오를
>  네가 직접 클릭해 끝까지 가봐. 막히면 고치고, **완주될 때까지 반복**해."

## 출처
- https://code.claude.com/docs/en/best-practices
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
