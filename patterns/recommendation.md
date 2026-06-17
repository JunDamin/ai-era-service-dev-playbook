# 추천 (Recommendation, Type A)

> **한 줄:** 사용자 상황을 받아 '받을 수 있는 것'을 정리해 신청 행동까지 연결한다. *배제가 위험한 도메인(복지 등)은 "추천 TOP-N"이 아니라 "완전 열거 + 비대칭 분류"* → 심화 ⓐ.

## 언제 쓰나
- 복지·지원사업 추천, "나에게 맞는 ○○ 찾기"류

## 입력 계약 (Input)
- 선택형 우선: **지역**(드롭다운) · **대상 유형**(멀티선택) · **가구/소득 구간**(선택)
- 자연어는 보조. 받은 값은 `session_state` 저장 → **재입력 금지**(Rule 3)
- **미입력 처리:** 조건 불명이면 후보를 보수적으로 제외하거나 확인 라벨로 — 유형마다 다르다(→ `README.md` 빈칸 비대칭 표)

## 처리 (파이프라인 내 역할)
- **Context Extraction**: 입력 → 구조화 프로필
- **Candidate Discovery**: 고정 데이터(`data-patterns/welfare_sample.json`)에서 자격 후보 필터(코드로)
- **Recommendation**: 우선순위 정렬 + **Confidence**(확정/높음/중간/확인 필요)
- **Explanation**: 왜 추천되는지 1~2줄

## 산출물 (Artifact)
- **추천 카드**: 혜택명 · 핵심혜택 · 신청방법 · 제출서류 · 기한 · **출처 링크**
- 조합: **+ Type D**(문서생성) → 신청 준비서/체크리스트 PDF

## A형 심화 — 완전 열거 + 비대칭 정확도 + 택1 + 벌크 (welfare-finder 환류)
> *배제가 틀리면 안 되는* 도메인(복지)에선 **"추천 TOP-N"이 아니라 "완전 열거 + 비대칭 분류"**. 아래는 *방법·의사코드*다 — 코드 반입이 아니라 당일 재현용으로 외운다.

### ⓐ 3구간 비대칭 분류 (`judge`)
후보를 셋으로: **✅확실 / 🔍확인필요 / ❌숨김.** 핵심 = *숨김(배제)은 100% 확신할 때만.*
```
if 명시적_분기_불일치(care_type 등): → hidden        # 명시 카테고리 위배
if 켠_상황칩과_태그_안겹침:          → 후보 아님
if 소득_명백초과(knockout, 아래):    → hidden
if 검증_큐레이션 and 태그매칭 and not 소득초과: → ok
if 정형_high신뢰 and 태그매칭 and 소득명확OK:    → ok
else:                                → check        # 매칭됐으나 애매 = 전부 여기(놓침 0)
```
- **소득 knockout(배제선)**: `median_pct` 있고 `confidence=high`이고 **사용자 소득 하한 ≥ 그 상한**일 때만. 사용자가 "중위 N% *이하*"를 골랐으면 *실제값을 모르므로 하한이 없다 → 배제 불가*(오직 "*초과*" 선택만 하한을 만든다). ⇒ **미입력·모름은 절대 배제 안 함.**
- 정렬: 검증 > 고신뢰 > 그외, 전국 먼저.

### ⓑ 택1 (동시수급 배제, `pairExcluded`)
- *확실한* 양자택일 쌍만 데이터로(`exclusion_pairs`: `{a, b, label}`). ✅군에 둘 다 들면 **라디오로 인접 배치**, 안 고른 쪽은 회색+합산 제외. 애매한 배제는 **⚠️ 경고만**(숨기지 말 것).

### ⓒ 벌크 서류 (`mergeBulk`)
- ✅군의 구비서류를 합쳐 **중복 제거** → 2층: **확정**(검증 or 고신뢰=양식파일) / **옵션**(저신뢰=본문언급). 사용처 빈도순. "이 N종이면 M곳" 카피.
- **NOISE 필터**: 서류명이 *안내·지침·계획·운영·매뉴얼* 류면 참고자료로 보고 서류에서 제외(잘못 준비 방지).

### ⓓ 데이터 shape (자격 정형화)
`{ income:{type, median_pct, bound, confidence}, age:{min,max,unit}, categories:[{cat}], exclusions:[{what}], documents:[{std_name, source: 양식파일|본문언급, confidence}], confidence }`
- **추출=사실만**(근거 원문 보존), **판정=코드**(§5 판정 안 함). 서류는 표준 명칭으로 정규화(=중복제거 키).

### ⓔ 생애주기 변주 (리드 컨셉)
- 같은 완전열거를 **시점별로 분할**(이번 달 / 출산 전·후 / 6개월 / 1년) — *시간 정렬이지 버림이 아니다*(각 시점이 완전목록). 마감 임박은 **손실 프레임**으로 행동 유도(단, "받는다/손실 확정" 단정 ❌).

## 조합 예시
- "맞춤 정부 혜택 찾기" = **A 추천 + D 신청가이드**
- "임산부 원스톱" = **C 타임라인 + A 시기별 추천**(= ⓔ 생애주기)

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
- 구조화 출력/few-shot → `prompts/README.md` §1·§2
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
