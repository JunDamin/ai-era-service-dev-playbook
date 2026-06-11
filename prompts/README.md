# prompts — 프롬프트 패턴 (한 파일)

> 근거: Anthropic 프롬프트 엔지니어링 docs(1차) · GitHub Spec Kit(1차).

## 1. XML 태그 구조화
- 내용 유형별로 **태그로 감싼다**: `<instructions>` · `<context>` · `<input>` · `<data>` → 오해↓.
- **일관·서술적 태그명**, 자연 계층은 네스팅(`<documents>` > `<document index="n">`).
```
<instructions>… 역할·제약·금지 …</instructions>
<input>{{사용자 입력}}</input>
<data>{{고정 데이터}}</data>
출력(JSON): { … }
```

## 2. Few-shot (예시 3~5개)
- **3~5개** 예시가 출력 형식·톤·구조를 가장 신뢰성 있게 조향.
- 예시는 **관련(실사용 반영) · 다양(엣지케이스) · 구조화**(`<example>`/`<examples>`).
- Claude에게 예시 **생성·평가**도 시킬 수 있다.

## 3. 시스템 프롬프트 '적정 고도'
- 브리틀한 if-else도, 모호한 고차원 지침도 아닌 **중간 고도**(Goldilocks).
- 섹션화: `<background_information>` · `<instructions>` · `## Tool guidance` · `## Output`.
- **기대 행동을 온전히 그리는 최소 정보**가 목표(과잉·부족 모두 실패).

## 4. 스펙 주도 슬래시 커맨드
- 4단계(좌→우 의존): **/specify**(무엇·왜) → **/plan**(설계) → **/tasks**(분해) → **/implement**(구현). 스펙 = 계약·진실 원천. 자세히: `method/README.md` §2.

## 출처
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://github.com/github/spec-kit
