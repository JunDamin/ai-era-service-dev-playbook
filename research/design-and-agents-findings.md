# 딥리서치 4차: 디자인 구체 + 멀티에이전트/바이브코딩 (갭 보강)

> 이전 라운드 검증 0였던 두 영역을 1차·피어리뷰 출처로 보강. (조사일: 2026-06)

## A. 디자인 (AI 슬롭 회피) — 검증 高
1. **8pt/4pt 간격 그리드** — 임의 px 대신 양자화된 간격이 '디자인된 UI vs AI 기본값'을 가른다. (아이콘·타입은 4pt) [Material](https://material.io/design/layout/spacing-methods.html)
2. **디자인 토큰 = 단일 진실원천(SSOT)** — 색·타이포·간격을 토큰(이름=값)으로 한 곳에 → 중앙 변경=전체 반영. W3C DTCG가 JSON 포맷($value/$type) 표준화(2025.10 **커뮤니티그룹** 스펙, *W3C 표준 아님*). shadcn/ui는 시맨틱 CSS 변수로 구현(`background/foreground`, `primary/primary-foreground` 쌍). [shadcn](https://ui.shadcn.com/docs/theming) · [DTCG](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
3. **WCAG 2.1 AA 대비** — 본문 **4.5:1**, 큰 글자(18pt/14pt bold) 3:1. 저대비 슬롭을 막는 객관 기준. [WCAG 1.4.3](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

## B. 멀티에이전트 / 바이브코딩 — 검증 高
4. **오케스트레이터-워커** — 리드가 계획·위임, 서브에이전트는 병렬 실행이나 **동기 대기**. 각 서브에이전트엔 *목표·출력형식·도구/출처 안내·경계* 필요. [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
5. **언제 이득/손해 + 비용** — breadth-first·병렬·단일 컨텍스트 초과 작업엔 이득 / **대부분의 코딩엔 손해**(병렬화 적고 실시간 조율 약함). 비용: 단일 에이전트 챗 대비 **~4x 토큰**, 멀티 **~15x**, **토큰량이 성능변동의 80% 설명**(BrowseComp). 고가치 작업만 정당. [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
6. **더 많은 에이전트 ≠ 더 좋음(MAST)** — 멀티에이전트 이득은 종종 미미, 실패는 **14모드/3범주**(명세·시스템설계 / 에이전트 간 정합 / 검증·종료). 단순 처방으론 부족, 구조적 해법 필요. [MAST arXiv 2503.13657](https://arxiv.org/abs/2503.13657)
7. **바이브 엔지니어링(검증 규율)** — 무책임한 '바이브코딩' vs 책임지는 '바이브 엔지니어링'을 가르는 건 **검증·책임**. AI는 기존 역량을 *증폭*. 핵심 규율: 자동 테스트·사전 계획·문서·버전관리·CI·코드리뷰·수동 QA·프리뷰 배포. [Simon Willison](https://simonwillison.net/2025/Oct/7/vibe-engineering/)
8. **테스트가 최대 enabler** — 견고한 자동 테스트 스위트가 에이전트 코딩의 단일 최대 조력자, **test-first/red-green**이 자기수정 루프. ⚠️ 단 (a) AI생성 테스트는 *거짓 자신감*(높은 커버리지·낮은 mutation) → 의도된 동작을 검증해야, (b) 어떤 테스트를 볼지 안 정한 순진한 TDD 프롬프트는 회귀↑('TDD 프롬프트 역설'), (c) 단위테스트 통과만으론 불충분 → **브라우저/결과 수준 검증** 추가. [Simon Willison](https://simonw.substack.com/p/agentic-engineering-patterns)

## 주의
- Material URL은 M2(레거시)지만 8dp 원칙 유효(미세요소 4dp). DTCG는 커뮤니티그룹 스펙(표준 아님). shadcn은 관례(강제 아님).
- Willison은 권위 실무자 의견(피어리뷰 인과 아님). 80% 수치는 BrowseComp 한정.
- METR(2025.7): 숙련 개발자 AI로 19% 느려진 RCT도 있음 → "전문가 증폭"의 크기는 맥락의존(핵심 '규율 의존' 논지는 강화).
