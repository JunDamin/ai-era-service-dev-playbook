# design/design-system — 'AI 슬롭' 회피

> 근거: Material(8dp)·shadcn·W3C(WCAG·DTCG) 1차 — 4차 리서치 검증. 핵심: **일관성·절제·위계**. 구체 값은 `design-tokens.md`.

## 슬롭이 생기는 이유 → 처방 (근거)
| 증상 | 처방 | 근거 |
|---|---|---|
| 제멋대로 간격·크기 | **8pt 그리드 + 타이포 스케일** 고정(임의 px ❌) | Material 8dp |
| 색 남발·**저대비** | 중립 베이스 + 시그널 색만, **본문 4.5:1**(큰글자 3:1) | WCAG 1.4.3 |
| 강조 과다 | 화면당 **강조 소수**, 위계 분명 | lessons/UX(위계) |
| 컴포넌트 제각각 | **컴포넌트 시스템**(shadcn/ui·Tailwind) + 시맨틱 토큰 | shadcn |
| 무국적 기본 룩 | **디자인 토큰 1세트**(SSOT)로 정체성 | DTCG |

## AI에게 디자인 시킬 때
- "임의로 정하지 말고 **`design-tokens.md`를 따르라**" + 구체 토큰(색/간격/스케일)을 명시.
- 컴포넌트는 검증된 라이브러리(shadcn/ui 등) + **시맨틱 토큰**으로 통일 → 일관성 자동.
- **대비 체커**로 토큰 색쌍 검증(저대비 차단). 한 화면 = 강조 1~2개.

## 4시간 적용
- 시작 시 토큰·테마(`config.toml`) 적용 → 이후 디자인 결정 최소화(Defaults-first).

## 출처
- https://material.io/design/layout/spacing-methods.html · https://ui.shadcn.com/docs/theming
- https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
> ⚠️ Material URL은 M2(레거시)지만 8dp 원칙 유효 · DTCG는 커뮤니티그룹 스펙.
