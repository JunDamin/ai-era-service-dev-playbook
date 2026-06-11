# stack — 빠른 프로토타이핑 (Streamlit 단일파일)

> 근거: Streamlit 공식 docs(1차) — 3차 리서치 검증. 출발점 코드: `stack/templates/recommend_app.py`.

## 0. 스택 선택 규칙 — 프레임워크는 아이디어 크기에 비례 (3-way 드라이런 실측)
> 같은 문제(민원 라우터)를 세 스택으로 빌드해 측정. **속도는 셋 다 분 단위로 충분히 빨라 승부처가 아니다** — 가르는 축은 **LLM 호출 가능 여부**와 **디자인 천장**.

| 아이디어가 요구하는 것 | 스택 | 실측·근거 |
|---|---|---|
| 폼+결과 최소 코드 · 빠른 내부 검증 | **Streamlit 단일 파일 (기본값)** — §1~5 | 위젯=한 줄 최속. 단 **디자인 천장 낮음**(테마까지만, 세밀 CSS 곤란) |
| **LLM 호출 + 제품감 둘 다** (대부분의 대회 데모) | **FastHTML+MonsterUI (적극 검토)** — §6 | 재구현 4분57초·**환각 0**(llms-ctx 하네스 필수). Python·uv 유지, 진짜 HTML이라 `design/tokens.css` 주입 시 천장 무제한 |
| 코드 로직만으로 충분(LLM 불요) · 최고 제품감 | **정적 HTML+JS 단일 파일** | 재구현 2분30초·의존성 0. ⚠️ **LLM 서버 호출 불가**(키 노출) — 분류·계산·체크리스트(C형)에 최적 |
| 복잡한 클라이언트 상호작용 · 다화면 제품 | React/Next 등 — 이미 4시간 프로젝트가 아닐 수 있음, 범위 재점검 | 미측정 |
- **규칙:** 기본값에서 벗어나려면 **이유를 한 문장으로**(`02-template` §11에 기록). 못 쓰면 기본값.
- **디자인 천장은 스택이 아니라 토큰이 결정** — `design/tokens.css`를 주입하면 정적 HTML과 FastHTML은 같은 룩(드라이런 검증). Streamlit만 주입이 제한적.
- 어떤 스택이든 유지: 세션/입력 상태 저장(Rule③) · 키 없이 동작(mock) · 출력 계약(10초 가치·Artifact).

## 1. 단일파일 패턴 (<50줄로 챗 앱)
- **왜:** 세팅 최소 → 4시간에 최적. 무거운 프레임워크(LangGraph 등) 불필요.
- **구조:** `session_state` 히스토리 초기화 → 표시 루프 → `st.chat_input` → LLM 호출(stream) → `st.write_stream`.
- **4시간:** `recommend_app.py`를 복제해 입력·데이터·프롬프트만 교체.

## 2. 상태 = `st.session_state`
- **왜:** Streamlit은 상호작용마다 **위→아래 전체 재실행**(rerun). 그냥 변수는 매번 초기화됨.
- **어떻게:** 유지할 값(히스토리·입력)은 `st.session_state`에 저장(없으면 `setdefault`). = 자동저장/재입력 방지.

## 3. 스트리밍
- **왜:** 토큰 단위 출력 = 체감속도↑(빈 스피너 대안).
- **어떻게:** `st.write_stream(...)`은 제너레이터/OpenAI·LangChain Stream을 그대로 받음(`stream=True`).

## 4. 캐싱 (rerun 모델 대응)
- **왜:** 매 rerun마다 느린 함수 재실행·객체 재생성 방지.
- **어떻게:** **`st.cache_data`가 기본**(직렬화 데이터, 복사본 반환 → 변이/경쟁 안전). 모델·DB연결 등 직렬화 불가 전역 자원만 `st.cache_resource`.
- **함정:** `cache_resource`는 객체 자체를 공유 → **여러 세션 변이 시 손상·크래시** 위험. 헷갈리면 `cache_data`.

## 5. 시크릿 / API 키
- **왜:** 키를 코드·커밋에 두면 유출.
- **어떻게:** `st.secrets` + `.streamlit/secrets.toml`(반드시 `.gitignore`). 배포는 Community Cloud Secrets 콘솔.
- **4시간:** 키는 `secrets.toml` 또는 환경변수. 보일러플레이트는 키 없으면 mock으로 동작.

## 6. FastHTML+MonsterUI 패턴 (대안 스택 — LLM+제품감)
- **하네스 먼저(필수):** 신생 프레임워크라 학습 커버리지가 얇다 → 코딩 전에 **공식 LLM 문서를 컨텍스트로 주입**: `https://fastht.ml/docs/llms-ctx.txt`(+ MonsterUI README). 이걸로 드라이런에서 **환각 0** 달성 — 생략하면 FastAPI 패턴과 혼동하는 환각이 알려진 문제.
- **골격:** `fast_app(hdrs=(Theme.slate.headers(), <tokens.css 주입>))` → `@rt` 라우트 → FT 컴포넌트(위치 인자=자식, 명명 인자=속성, `cls`=class) → HTMX 부분 업데이트(`hx_post=fn, hx_target="#id"`).
- **디자인:** `design/tokens.css`를 `Style()`로 주입 → 정적 HTML과 동급 룩. **커스텀 클래스는 `.pb-` 프리픽스** — FrankenUI가 `.hero` 같은 클래스를 선점하고 있어 충돌하면 레이아웃이 포개진다(실증).
- **로직/UI 분리 동일 적용:** 로직은 모듈 레벨, `serve()`는 `__main__` 가드 → 2단계 검증 그대로.

### FastHTML/uvicorn 함정 (드라이런 실증)
- **데모는 `serve(reload=False)`** — 리로더(WatchFiles)는 ① OneDrive 폴더에서 변경 감지를 누락하고 ② 죽일 때 **워커 자식이 포트를 물고 살아남는다**(Windows 좀비 — 새 서버와 동시 bind되어 구버전이 응답). 수정 후엔 그냥 재시작이 빠르다.
- **좀비 사냥보다 포트 변경이 싸다** — 포트가 이상하면(죽은 PID가 LISTEN에 박제) 포렌식 말고 새 포트로 옮겨라. 죽일 땐 PID가 아니라 **커맨드라인 매칭**으로(`Win32_Process WHERE CommandLine LIKE '%프로젝트명%'`).
- **브라우저 캐시 주의** — 검증 중 구버전이 보이면 `?v=N` 캐시버스터로 새로고침.

## 흔한 함정
- rerun을 잊고 일반 변수 사용 → 상태 사라짐(→ session_state)
- 무거운 객체를 매번 생성 → 느림(→ cache_resource)
- 키 하드코딩/커밋(→ secrets)
- **위젯 key는 생성 후 수정 금지** — 버튼 콜백에서 `st.session_state.addr = …`처럼 *이미 그려진* 위젯의 key를 바꾸면 `StreamlitAPIException`. **처방:** 임시 키(`_pending_addr`)에 담고 `st.rerun()` → 다음 런에서 **위젯을 그리기 전에** 주입.
- **포트 충돌로 '엉뚱한 앱'이 뜸** — `0.0.0.0:8501`과 `127.0.0.1:8501`에 서로 다른 앱이 동시에 물릴 수 있어, localhost로 열면 이전 앱이 보인다(데모 사고 1순위). **처방:** 앱마다 포트 고정(`.streamlit/config.toml`의 `server.port`) + 띄운 뒤 **페이지 타이틀로 내 앱인지 확인**, 의심되면 새 포트.
- **로직과 UI를 한 덩어리로** — 모듈 레벨 함수 + `main()`/`__main__` 가드로 분리해야 UI 없이 로직 테스트 가능(→ `claude-craft/verification-loop.md` 2단계 검증).

## 출처
- https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps
- https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
- https://docs.streamlit.io/develop/api-reference/write-magic/st.write_stream
- https://docs.streamlit.io/develop/concepts/architecture/caching
- https://docs.streamlit.io/develop/concepts/connections/secrets-management
