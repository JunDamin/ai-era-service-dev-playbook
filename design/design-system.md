# design/design-system — 'AI 슬롭' 회피

> ⚠️ **잠정(실무 출처 기반, 검증 보강 필요).** 핵심: **일관성·절제·위계**. 구체 값은 `design-tokens.md`.

## 슬롭이 생기는 이유 → 처방
| 증상 | 처방 |
|---|---|
| 제멋대로 간격·크기 | **8pt 그리드 + 타이포 스케일** 고정 |
| 색 남발·저대비 | 중립 베이스 + **시그널 색만**, 대비 확보 |
| 강조 과다 | 화면당 **강조 소수**, 위계 분명 |
| 컴포넌트 제각각 | **컴포넌트 시스템**(shadcn/ui·Tailwind 등) 일관 사용 |
| 무국적 기본 룩 | **토큰 1세트**로 정체성 부여 |

## AI에게 디자인 시킬 때
- "임의로 정하지 말고 **`design-tokens.md`를 따르라**" + 구체 토큰(색/간격/스케일)을 프롬프트에 명시.
- 컴포넌트는 검증된 라이브러리(shadcn/ui 등)로 통일 → 일관성 자동 확보.
- 한 화면 = 한 주인공(강조 1~2개).

## 4시간 적용
- 시작 시 토큰·테마(`config.toml`) 적용 → 이후 디자인 결정 최소화(Defaults-first).

> 출처(잠정): mindstudio(claude design), figma(better AI prompts), shadcn/tailwind — `research/playbook-gaps-findings.md`.
