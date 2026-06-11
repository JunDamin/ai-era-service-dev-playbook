---
name: design-polish
description: Streamlit 앱의 UI/디자인을 만들거나 다듬을 때 사용. "디자인 다듬어줘", "예쁘게", "폴리시", "AI 슬롭 같다", 데모 직전 마감 등에서 호출. 디자인 토큰·테마·라이팅·슬롭 회피를 한 번에 적용한다.
---

# design-polish — 플레이북 디자인 마감 스킬

> 목적: **결정 없이** 이 리포의 디자인 기본값을 일괄 적용해, 4시간 안에 'AI 슬롭'이 아닌 화면을 만든다.
> 원천 문서(충돌 시 그쪽이 진실): `design/design-tokens.md` · `design/design-system.md` · `lessons/ux.md` §7-8

## 순서 (위에서 아래로 한 번)

### 1. 테마 — 앱마다 `.streamlit/config.toml` 먼저
```toml
[theme]
primaryColor = "#15314f"        # 토큰 primary(navy) — 문제 성격에 맞으면 교체 가능
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f4f7fb"   # 토큰 tint
textColor = "#1b2330"           # 토큰 ink
font = "sans serif"

[server]
port = 85XX   # 앱마다 다른 포트 고정(데모 사고 예방 — stack/fast-prototyping.md 함정 참조)
```

### 2. 토큰 점검 (design-tokens.md)
- 간격: **8pt 그리드**(4·8·12·16·24·32·48)만. 임의 px ❌
- 타이포: 12/14(본문)/16/20/26/34 스케일. 본문 400·강조 700·제목 800
- 색: **중립 베이스 + 시그널 색만**(정상 `#1d8a3c`·주의 `#d99413`·경고 `#cc2f2f`). 색은 의미로만
- 대비: 본문 4.5:1 이상(특히 muted·accent on 흰 배경)

### 3. 슬롭 회피 점검 (design-system.md 표)
- [ ] 화면당 **강조(고대비·볼드) 1~2개**뿐인가
- [ ] 같은 역할의 요소가 같은 모양인가(카드 radius 6px·경계 1px 통일)
- [ ] 그림자·이모지·색 남발이 없는가

### 4. 라이팅 스윕 (lessons/ux.md §7-8 — 토스 기준)
- 버튼: 다음 화면이 예측되는 동사("확인" ❌ → "체크리스트 다운로드" ✅)
- 모든 문구: 잡초 단어 제거 · 한 문장 한 메시지 · 해요체 · 강요/공포 ❌
- 에러·폴백·빈 상태: **무엇+왜+해결** 3요소("실패" ❌ → "키가 없어 예시 모드예요. 키 설정 후 실제 결과를 볼 수 있어요" ✅)

### 5. 출력 계약 확인 (CLAUDE.md)
- 진입 10초 안에 가치(빈 화면 ❌ — 예시 프리필/데모 칩)
- 결과는 Artifact(다운로드·복사)로 끝맺음 + "다음 행동" 안내
- 모바일: `layout="centered"` 기준 좁은 폭에서 컬럼 깨짐 확인

## 검증
브라우저로 열어 스크린샷 1장 → 위 체크리스트와 대조. 통과 못 한 항목만 고치고 재확인.
