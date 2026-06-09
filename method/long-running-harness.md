# method/long-running-harness — 장시간 빌드 하네스

> 근거: Anthropic(1차).

## 패턴 (문제가 커지지 않게)
- **요구사항 파일**(전 기능 'failing')을 먼저 → ground truth. 한 방에 끝내거나 조기 완료 선언하는 것을 막음.
- **end-to-end 검증** — 브라우저로 사람처럼. 단위테스트·curl로는 '실제로 작동'을 못 잡음.
- **git 커밋(서술적) + 진행 파일** → 세션 간 연속성(새 세션은 기억 0).

## 4시간 적용
- 0–30분 `requirements.md` 작성 → 단계마다 커밋 + 진행 메모.

## 출처
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
