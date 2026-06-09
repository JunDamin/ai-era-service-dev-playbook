# 딥리서치: 빠르게 만드는 앱을 위한 UX·제품 설계 원칙

> 29개 출처 → 139개 주장 → 25개 3표 검증(전부 확정). **거의 전부 Nielsen Norman Group(NN/g) 1차 출처.** (조사일: 2026-06)

## 검증된 발견 (신뢰도 高, 출처 포함)

1. **시스템 상태 가시성**(휴리스틱 #1) — 합리적 시간 내 적절한 피드백. [NN/g 10 heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [visibility](https://www.nngroup.com/articles/visibility-system-status/)
2. **오류 예방 > 좋은 오류 메시지**(#5) — 좋은 기본값·제약·확인으로 문제 자체를 방지. [NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/)
3. **인지 > 회상**(#6) — 외워 타이핑하지 말고 보이는 선택지로(선택>입력 근거). [NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/)
4. **심미-사용성 효과** — 보기 좋으면 '사소한' 문제는 용서됨(큰 결함은 못 가림). [NN/g](https://www.nngroup.com/articles/aesthetic-usability-effect/)
5. **폼 ROI** — 가이드라인 준수 폼 첫시도 성공 **78% vs 위반 42%(거의 2배)**. [NN/g](https://www.nngroup.com/articles/web-form-design/), Seckler et al. CHI 2014
6. **플레이스홀더 금지 → 영구 레이블** — 사라져서 기억부담·검증불가. 필드 밖 레이블+힌트. [NN/g placeholders](https://www.nngroup.com/articles/form-design-placeholders/)
7. **인라인 검증은 on-blur** — 타이핑 중 조기검증 금지, 필드 옆 메시지, 실시간은 비번 체크리스트류만. [NN/g errors](https://www.nngroup.com/articles/errors-forms-design-guidelines/), [Baymard](https://baymard.com/blog/inline-form-validation)
8. **점진적 공개 + 한 페이지 한 질문** — 고급은 토글 뒤로, 긴 폼은 위저드. [NN/g](https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/), [GOV.UK](https://designnotes.blog.gov.uk/2015/07/03/one-thing-per-page/)
9. **대시보드 한눈에 + 전주의적 처리** — 정량은 **길이·2D위치**로(면적/파이 부정확). [NN/g](https://www.nngroup.com/articles/dashboards-preattentive/), Cleveland & McGill 1984
10. **시각적 위계** — 중요도 순으로 눈을 유도(명도·채도 대비, 볼드). 강조는 소수만. [NN/g](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)
11. **F-패턴에 '맞서' 설계** — 헤딩·볼드·앞부분 배치·불릿(사용자는 큰 덩어리를 놓침). [NN/g](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)
12. **복잡한 앱 = 단계적 공개(staged)** — 관련 항목 선택 후에만 세부 옵션 노출. [NN/g](https://www.nngroup.com/articles/complex-application-design/)

## ⚠️ 갭 (적대검증 통과 주장 없음 → 보강 필요)
- **(5) AI/대화형 UX**, **(6) MVP 스코핑**: 1차 검증 주장 0건. 단 관련 NN/g·실무 출처는 확보(아래) → `AIChat.md`·`MVP.md`는 *잠정*으로 표기.
- **'3클릭 규칙'은 미신** — NN/g·UX Myths가 근거 약함을 지적. **규칙으로 채택 금지.** [NN/g](https://www.nngroup.com/articles/3-click-rule/), [UX Myths](https://uxmyths.com/post/654026581/myth-all-pages-should-be-accessible-in-3-clicks)
- F-패턴 보편성은 2-1(서식 없는 텍스트·저몰입에서). '항상 F로 읽음'이 아니라 '맞서 설계'가 올바른 적용.

## 보강 리서치 후보 (AIChat/MVP용 확보 출처)
- 응답시간 한계 0.1s/1s/10s — [NN/g](https://www.nngroup.com/articles/response-times-3-important-limits/) · Doherty <400ms — [Laws of UX](https://lawsofux.com/doherty-threshold/)
- AI를 전지적 오라클로 제시 말 것 — [NN/g AI Magic 8-Ball](https://www.nngroup.com/articles/ai-magic-8-ball/) · 설명가능성 — [NN/g Explainable AI](https://www.nngroup.com/articles/explainable-ai/)
- 스코프/피처 크리프 방지 — [ProductPlan](https://www.productplan.com/learn/scope-creep/), [LogRocket](https://blog.logrocket.com/product-management/what-is-feature-creep-how-to-avoid/)
