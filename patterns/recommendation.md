# 추천 (Recommendation, Type A)

> **한 줄:** 사용자 상황을 받아 '받을 수 있는 것'을 우선순위로 추천하고, 신청 행동까지 연결한다.

## 언제 쓰나
- 복지·지원사업 추천, "나에게 맞는 ○○ 찾기"류

## 입력 계약 (Input)
- 선택형 우선: **지역**(드롭다운) · **대상 유형**(멀티선택) · **가구/소득 구간**(선택)
- 자연어는 보조. 받은 값은 `session_state` 저장 → **재입력 금지**(Rule 3)

## 처리 (파이프라인 내 역할)
- **Context Extraction**: 입력 → 구조화 프로필
- **Candidate Discovery**: 고정 데이터(`data-patterns/welfare_sample.json`)에서 자격 후보 필터(코드로)
- **Recommendation**: 우선순위 정렬 + **Confidence**(확정/높음/중간/확인 필요)
- **Explanation**: 왜 추천되는지 1~2줄

## 산출물 (Artifact)
- **추천 카드**: 혜택명 · 핵심혜택 · 신청방법 · 제출서류 · 기한 · **출처 링크**
- 조합: **+ Type D**(문서생성) → 신청 준비서/체크리스트 PDF

## 조합 예시
- "맞춤 정부 혜택 찾기" = **A 추천 + D 신청가이드**
- "임산부 원스톱" = **C 타임라인 + A 시기별 추천**

## Claude 프롬프트 (복붙)
```
<instructions>
아래 사용자 프로필로 후보 목록에서 받을 수 있는 항목을 골라
우선순위·Confidence·신청 행동을 제시하라.
- 자격 '판정'은 하지 말 것. 불확실하면 confidence="확인 필요"와 확인할 항목을 명시.
- data에 없는 사실은 지어내지 말 것(없으면 '확인 필요').
</instructions>
<user_profile>{{profile}}</user_profile>
<candidates>{{filtered_welfare_json}}</candidates>
출력(JSON):
[{ "name","benefit","how_to_apply","documents","deadline","source_url","confidence","why" }]
```

## 데이터
- `data-patterns/welfare_sample.json` — 서비스명·대상·혜택·신청방법·서류·문의·URL (고정 데이터)

## 근거 / 출처
- 행동>정보·추천→결과물 = CLAUDE.md Rule 1·4
- 구조화 출력/few-shot → `prompts/xml-structure.md`, `prompts/few-shot.md`
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
