# design/design-tokens — 기본 디자인 토큰 (Defaults-first)

> **물어보지 말고 이 기본값을 적용한다.** 바꾸고 싶을 때만 override. (테마: `../.streamlit/config.toml`)
> **실행 가능한 구현체: [`tokens.css`](tokens.css)** — 스택 무관(정적 HTML=`<link>`, FastHTML=`Style()` 주입). 같은 토큰을 어느 스택에 꽂아도 일관된 룩이 나온다(스택 비교 드라이런으로 검증). 클래스는 `.pb-` 프리픽스(UI 프레임워크 충돌 방지).

## 왜 토큰인가 (단일 진실원천)
색·타이포·간격을 **토큰(이름=값)으로 한 곳에서** 정의 → 중앙에서 바꾸면 전체 반영(일관성↑). W3C DTCG가 JSON 포맷($value/$type)을 표준화. shadcn/ui는 **시맨틱 CSS 변수**로 구현.

## 색 — 시맨틱 + 시그널
| 역할 | 값 |
|---|---|
| primary(navy) | `#15314f` · navy2 `#2a5180` |
| ink/본문 | `#1b2330` · muted `#5d6877` |
| line/경계 | `#d9e1ea` · tint(보조배경) `#f4f7fb` · bg `#ffffff` |
| accent | `#c2741a` (강조·큰 글자 위주) |
| signal | 정상 `#1d8a3c` · 주의 `#d99413` · 경고 `#cc2f2f` · 확인필요(info) `#2a6fb0` |
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

## 색맹 접근성 + 도메인 톤 (복지/안전)
- **색만으로 판단 금지(색맹 ~남성 8%).** 신호·등급은 **색 + 아이콘 + 텍스트**를 항상 병기(예 ✅"확실" / 🔍"확인 필요" / ❌"해당 없음", 🔴"위험 높음"). → 정부·디지털약자 포용·심사 체험 신뢰에 필수.
- **복지 톤(안심·따뜻·신뢰)**: 베이스 신뢰 네이비(`--pb-navy`) + 따뜻 악센트(앰버 `--pb-accent`/그린 `--pb-ok`). **3구간: ✅확실=ok(green) / 🔍확인필요=info(blue `--pb-info`, *빨강 금지*) / ❌숨김=muted(회색)** — 숨김은 *위험*이 아니라 *해당 없음*이라 빨강 ❌. 경보 빨강 남발·보라 그라데이션(AI 슬롭) 회피.
- **안전 톤(명료·신호 위계)**: 신호 trio(`ok`녹/`warn`주/`bad`적)를 *상태에만* 절제, 베이스는 차분(navy). **모름=warn(주황)**(거짓 안심 방지). 올-레드 패닉 금지.
- 같은 토큰, **악센트·지배 시맨틱만 도메인별로** 바꾼다(기본값 우선).

## 출처 (검증)
- 8dp 그리드 https://material.io/design/layout/spacing-methods.html
- 시맨틱 토큰 https://ui.shadcn.com/docs/theming · DTCG https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- 대비 https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
> ⚠️ DTCG는 W3C *커뮤니티그룹* 스펙(표준 아님), shadcn은 *관례*(강제 아님).
