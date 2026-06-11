# stack — 빠른 프로토타이핑 (Streamlit 단일파일)

> 근거: Streamlit 공식 docs(1차) — 3차 리서치 검증. 출발점 코드: `stack/templates/recommend_app.py`.

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
