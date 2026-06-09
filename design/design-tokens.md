# design/design-tokens — 기본 디자인 토큰 (Defaults-first)

> **물어보지 말고 이 기본값을 적용한다.** 바꾸고 싶을 때만 override. (테마: `../.streamlit/config.toml`)

## 왜 토큰인가 (단일 진실원천)
색·타이포·간격을 **토큰(이름=값)으로 한 곳에서** 정의 → 중앙에서 바꾸면 전체 반영(일관성↑). W3C DTCG가 JSON 포맷($value/$type)을 표준화. shadcn/ui는 **시맨틱 CSS 변수**로 구현.

## 색 — 시맨틱 + 시그널
| 역할 | 값 |
|---|---|
| primary(navy) | `#15314f` · navy2 `#2a5180` |
| ink/본문 | `#1b2330` · muted `#5d6877` |
| line/경계 | `#d9e1ea` · tint(보조배경) `#f4f7fb` · bg `#ffffff` |
| accent | `#c2741a` (강조·큰 글자 위주) |
| signal | 정상 `#1d8a3c` · 주의 `#d99413` · 경고 `#cc2f2f` |
- **시맨틱 페어링:** 표면색 ↔ 그 위 텍스트색을 쌍으로(예: primary ↔ primary-foreground). 컴포넌트는 토큰만 소비 → 테마 변경이 클래스 수정 없이 전파.

## 간격 — 8pt 그리드
`4 · 8 · 12 · 16 · 24 · 32 · 48` (기본 8) — **임의 px 금지.** 아이콘·타입 등 미세요소만 4pt.

## 타이포 — 스케일
`12 / 14(본문) / 16 / 20 / 26 / 34` (약 1.25배율) · 줄간격 1.4~1.5 · 본문 400 / 강조 700 / 제목 800

## 대비 — WCAG 2.1 AA
본문 **4.5:1**, 큰 글자(18pt/14pt bold) **3:1** 이상. → 토큰 색쌍을 **대비 체커**로 확인(특히 muted·accent on 흰 배경).

## 형태 / 규칙
- radius `6px` · 카드 경계 `1px line` · 그림자 최소.
- **강조(고대비·볼드)는 화면당 소수만** · **색은 의미로만**(시그널) · 간격·크기는 위 토큰에서만.

## 출처 (검증)
- 8dp 그리드 https://material.io/design/layout/spacing-methods.html
- 시맨틱 토큰 https://ui.shadcn.com/docs/theming · DTCG https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- 대비 https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
> ⚠️ DTCG는 W3C *커뮤니티그룹* 스펙(표준 아님), shadcn은 *관례*(강제 아님).
