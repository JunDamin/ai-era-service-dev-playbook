# DataInput — 입력 / 폼 교훈

> 근거: NN/g 폼 디자인(1차). **폼 ROI: 가이드라인 준수 시 첫시도 성공 78% vs 위반 42%(거의 2배).**

## 1. placeholder를 레이블로 쓰지 마라
- **왜:** 입력 시작하면 사라짐 → 기억 부담, 입력값으로 오인, 제출 전 검증 불가.
- **어떻게:** **필드 밖(위)에 항상 보이는 레이블** + 필요 시 힌트 텍스트. (플로팅 레이블은 차선)
- **4시간:** 모든 input에 `<label>` 명시. placeholder는 보조 예시로만.

## 2. 선택 > 입력 (인지 > 회상)
- **왜:** 외워 타이핑은 오류·부담. 보이는 선택이 빠르고 정확.
- **어떻게:** 드롭다운·칩·자동완성·날짜피커. 자유 텍스트는 최후.
- **4시간:** 우선순위 Click > Multi-select > Short text > 자연어.
- **어떤 컨트롤/구조를 쓸지**(평면·패싯·위저드·상황 트리·AI 자유서술)는 → **`input-patterns.md` 결정표**.

## 3. 검증은 on-blur (완료 후)
- **왜:** 타이핑 중 조기검증은 거슬리고 방해.
- **어떻게:** 필드를 떠날 때 검증, **메시지는 필드 옆/아래**, 명시적·정중·건설적("왜·어떻게 고치는지"). 실시간 검증은 비번 요건 체크리스트처럼 즉각 피드백이 이로울 때만.
- **4시간:** onBlur 검증 + 인라인 메시지. 긴 폼은 상단 요약 병행.

## 4. 빈 화면(empty state) 처리
- **왜:** 빈 화면은 막막함 → 이탈.
- **어떻게:** 예시 데이터/샘플 입력, "무엇을 하면 되는지" 안내, 첫 액션 버튼.
- **4시간:** 첫 진입에 예시 프리필 또는 "예시로 해보기" 버튼.

## 5. 한 페이지 한 질문 (긴 폼)
- **왜:** 한 화면 한 과제가 완료율↑·오류↓(GOV.UK).
- **어떻게:** 긴 폼은 위저드로 단계화, 단계당 한 질문/그룹.
- **4시간:** 입력이 5+개면 2~3단계 위저드로.

## 출처
- https://www.nngroup.com/articles/web-form-design/
- https://www.nngroup.com/articles/form-design-placeholders/
- https://www.nngroup.com/articles/errors-forms-design-guidelines/
- https://designnotes.blog.gov.uk/2015/07/03/one-thing-per-page/
- https://baymard.com/blog/inline-form-validation
