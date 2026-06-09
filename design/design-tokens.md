# design/design-tokens — 기본 디자인 토큰 (Defaults-first)

> **물어보지 말고 이 기본값을 적용한다.** 바꾸고 싶을 때만 override. (테마: `../.streamlit/config.toml`)

## 색 — 네이비 + 중립 + 시그널
| 역할 | 값 |
|---|---|
| primary(navy) | `#15314f` · navy2 `#2a5180` |
| ink/본문 | `#1b2330` · muted `#5d6877` |
| line/경계 | `#d9e1ea` · tint(보조배경) `#f4f7fb` · bg `#ffffff` |
| accent | `#c2741a` |
| signal | 정상 `#1d8a3c` · 주의 `#d99413` · 경고 `#cc2f2f` |

## 간격 — 8pt 그리드
`4 · 8 · 12 · 16 · 24 · 32 · 48` (기본 단위 8) — 임의 값 금지.

## 타이포 — 스케일
`12 / 14(본문) / 16 / 20 / 26 / 34` (약 1.25배율) · 줄간격 1.4~1.5
굵기: 본문 400 · 강조 700 · 제목 800

## 형태
radius `6px` · 카드 경계 `1px line` · 그림자 최소.

## 규칙 (항상)
- **강조(고대비·볼드)는 화면당 소수만.** (위계 = lessons/UX)
- **색은 의미로만**(시그널), 장식 남발 금지.
- 간격·크기는 위 토큰에서만 선택.

> 근거(잠정·실무): `research/playbook-gaps-findings.md` 참조.
