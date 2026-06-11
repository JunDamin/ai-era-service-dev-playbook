# 스킬 세팅 — 동봉 스킬 + 추가 설치 안내

> **스킬(Skill)** = Claude Code가 특정 작업에서 따르는 지침 묶음(SKILL.md). 트리거 조건에 맞으면 Claude가 자동/수동으로 불러 쓴다.
> 세팅이 복잡할 필요 없다 — **이 리포를 clone하면 동봉 스킬은 이미 세팅돼 있다.**

## 1. 동봉 스킬 (설치 불필요 — clone하면 끝)
리포 안 `.claude/skills/`에 있는 스킬은 **이 폴더에서 Claude Code를 열면 자동 발견**된다.

| 스킬 | 언제 발동 | 하는 일 |
|---|---|---|
| `design-polish` | UI를 만들거나 다듬을 때("디자인 다듬어줘", 데모 직전) | 테마·토큰·슬롭 회피·라이팅(토스 기준)·출력 계약을 한 번에 점검·적용 |

- 수동 호출: 프롬프트에 "design-polish 스킬로 다듬어줘" 또는 `/design-polish`.
- 확인: Claude에게 "사용 가능한 스킬 알려줘"라고 물으면 목록에 보인다.

## 2. 공식 플러그인 추가 설치 (선택 — 더 강한 디자인이 필요할 때)
Claude Code 공식 마켓플레이스에서 설치(1회, 약 1분):
1. Claude Code에서 `/plugin` 입력 → marketplace 탐색
2. 추천: **frontend-design**(독창적·고품질 프런트엔드 — 정적 HTML 산출물·발표자료에 유용), **playwright**(브라우저 검증 루프에 필요 — `claude-craft/verification-loop.md`)
- 동봉 `design-polish`와 역할 구분: **Streamlit 앱 마감 = design-polish**(이 리포 기본값) / **자유 HTML/리포트 디자인 = frontend-design 플러그인**.

## 3. 우리 스킬 추가하는 법 (팀 확장)
```
.claude/skills/<스킬이름>/SKILL.md
```
- frontmatter에 `name` + `description`(**트리거 조건을 구체적으로** — "~할 때 사용") 필수.
- 본문은 짧게: 순서·체크리스트·원천 문서 링크(중복 서술 대신 `design/` 등 원본을 가리켜라).
- 원칙: 스킬은 **플레이북 문서의 '실행 버튼'** — 내용의 진실원천은 항상 문서 쪽에 둔다.

## 함정
- 스킬이 안 보이면: Claude Code를 **리포 루트에서** 열었는지 확인(.claude/ 탐색 기준이 루트).
- 플러그인 스킬은 **설치한 사람에게만** 있다 — 팀 공유가 필요하면 동봉(`.claude/skills/`) 방식을 써라.
