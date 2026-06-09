# prompts/xml-structure — XML 태그 구조화

> 근거: Anthropic(1차).

- 내용 유형별로 **태그로 감싼다**: `<instructions>` · `<context>` · `<input>` → 오해↓.
- **일관·서술적 태그명**, 자연 계층은 네스팅(`<documents>` > `<document index="n">`).

예시:
```
<instructions>… 역할·제약·금지 …</instructions>
<input>{{사용자 입력}}</input>
<data>{{고정 데이터}}</data>
출력(JSON): { … }
```

출처: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
