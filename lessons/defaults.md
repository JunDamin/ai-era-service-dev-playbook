# Defaults — 기본값 · 점진적 공개 · 설정 최소화

> 근거: NN/g 인지부하 4원칙·점진적 공개(1차).

## 1. sensible defaults (좋은 기본값)
- **왜:** 사용자는 설정을 싫어한다. 좋은 기본값이 오류를 예방한다(휴리스틱 #5).
- **어떻게:** 가장 흔한 선택을 미리 선택해두고, 바꾸고 싶은 사람만 바꾸게.
- **4시간:** 모든 옵션에 default 지정. "설정 없이도 바로 작동"이 기본 상태.

## 2. 점진적 공개 (progressive disclosure)
- **왜:** 기본 화면에 주요 옵션만 → 학습 쉬움·과부하·오류↓.
- **어떻게:** 2차/고급 기능은 '더 보기/고급' 토글·하위 화면으로.
- **4시간:** 화면 첫 진입엔 핵심만. 고급은 접어두기.

## 3. 단계적 공개 (staged disclosure)
- **왜:** 복잡한 폼은 관련 항목 선택 후에만 세부를 보여주면 혼잡↓(기능은 유지).
- **어떻게:** 체크/스위치가 켜질 때만 관련 세부 옵션 노출.
- **4시간:** "○○ 포함" 체크 시에만 관련 입력란 등장.

## 4. 자동 저장 (autosave)
- **왜:** 사용자는 저장을 잊는다. 작업 손실 = 최악의 경험.
- **어떻게:** 입력 즉시/세션에 저장, "저장됨" 상태 표시(상태 가시성).
- **4시간:** `session_state`에 즉시 저장, 재입력 강요 금지(수정만 허용).

## 출처
- https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/
- https://www.nngroup.com/videos/progressive-disclosure/
- https://www.nngroup.com/articles/complex-application-design/
- https://www.nngroup.com/articles/ten-usability-heuristics/  (오류 예방: 기본값·제약)
