"""FastHTML 멀티페이지 위저드 — clone-and-go (LLM 연결, 키 없으면 mock)
실행: pip install python-fasthtml && python stack/templates/fasthtml_app.py → http://localhost:5025
언제 이걸 고르나: LLM 호출 + 제품감(토큰 CSS 천장) + 멀티페이지가 필요할 때 → stack/fast-prototyping.md §0·§6

⚠️ 빌드 전 하네스(필수): FastHTML은 신생이라 환각 위험 — 공식 LLM 문서를 먼저 컨텍스트에 넣어라.
   https://fastht.ml/docs/llms-ctx.txt  (이 절차로 드라이런 환각 0 실증)

기본값으로 박힌 메커니즘(도메인을 바꿔도 유지하라):
  · 라우트=페이지(One Thing Per Page, lessons/input-patterns P4) + 진행 표시
  · sess로 입력 누적(Rule③ 다시 묻지 않기 — 쿠키 ~4KB, 길면 키만 세션에)
  · 제출 전 confirm(check-answers) 페이지 + 단계별 수정 링크
  · 디자인 = design/tokens.css 주입(.pb-*) — 커스텀 클래스는 반드시 프리픽스(충돌 함정)
  · LLM은 mock 폴백(키 없이 동작) · 결과는 Artifact(다운로드)로 끝맺음
  · serve(reload=False) — uvicorn 좀비 리로더 함정 · 지도/3D 등은 Script(src=) 한 줄(§6)"""
import os, json, pathlib
from fasthtml.common import *

MODEL = "claude-sonnet-4-6"
TOKENS = (pathlib.Path(__file__).parent / ".." / ".." / "design" / "tokens.css").resolve().read_text(encoding="utf-8")

app, rt = fast_app(hdrs=(
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css"),
    Style(TOKENS),
    Style(".pb-prog{display:flex;gap:8px;margin-bottom:24px}.pb-prog span{flex:1;height:6px;border-radius:99px;background:var(--pb-line)}.pb-prog span.on{background:var(--pb-navy)}")))

# 질문(도메인에 맞게 교체) — 한 화면 하나
STEPS = [
    {"id": "who", "title": "어떤 상황인가요?", "kind": "radio", "options": ["옵션 A", "옵션 B", "옵션 C"]},
    {"id": "detail", "title": "조금 더 알려주세요", "kind": "text", "placeholder": "자유롭게 적어주세요 (예시를 placeholder로)"},
]


def _key():
    return os.environ.get("ANTHROPIC_API_KEY", "")


def make_result(answers):
    """결과 생성 — 계산·필터는 코드로, 설명만 LLM(키 없으면 mock)."""
    fallback = f"입력 요약: {answers.get('who','-')} / {answers.get('detail','-')} — (키 없음: mock 설명)"
    key = _key()
    if not key:
        return fallback
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=key)
        m = c.messages.create(model=MODEL, max_tokens=300, messages=[{"role": "user", "content":
            ("<instructions>입력을 2~3문장으로 요약·행동 제안. 지어내기 금지, 단정 판정 금지.</instructions>\n"
             f"<input>{json.dumps(answers, ensure_ascii=False)}</input>")}])
        return (m.content[0].text or "").strip() or fallback
    except Exception:
        return fallback


# ── 공통 셸 ──────────────────────────────────────────────────────
def shell(step, *content):
    total = len(STEPS) + 2  # 질문들 + confirm + result
    dots = Div(*[Span(cls="on" if i <= step else "") for i in range(total)], cls="pb-prog")
    return (Title("위저드 템플릿"),
            Div(Div(Div("서비스 이름", cls="pb-badge"), H1("한 줄 핵심 가치"),
                    P("첫 10초에 이해시킬 한 가지 — PROJECT.md §5 서비스 철학에서 가져와라."), cls="pb-hero"),
                dots, *content, cls="pb-wrap"))


def head(n, title, sub=""):
    return Div(Div(str(n), cls="pb-stepnum"), Div(H2(title), Div(sub, cls="pb-sub")), cls="pb-step")


# ── 질문 페이지(라우트=페이지) ───────────────────────────────────
@rt("/")
def index(sess):
    return step_page(sess, 0)


@rt("/step/{i}")
def step_page(sess, i: int):
    if i >= len(STEPS):
        return RedirectResponse("/confirm")
    s = STEPS[i]
    a = sess.get("answers", {})
    if s["kind"] == "radio":
        field = Div(*[Label(Input(type="radio", name="value", value=o, checked=(a.get(s["id"]) == o)), " " + o,
                            style="display:block;margin:8px 0") for o in s["options"]])
    else:
        field = Textarea(a.get(s["id"], ""), name="value", rows="4", cls="pb-i", placeholder=s.get("placeholder", ""))
    return shell(i, Div(
        head(i + 1, s["title"], "답은 자동 저장돼요 — 뒤로 가도 다시 묻지 않습니다."),
        Form(field, Button("다음", cls="pb-btn"),
             Hidden(str(i), name="i"), action="/save", method="post"),
        cls="pb-card"))


@rt("/save")
def save(sess, i: int, value: str = ""):
    sess["answers"] = sess.get("answers", {}) | {STEPS[i]["id"]: value}
    return RedirectResponse(f"/step/{i+1}", status_code=303)


# ── confirm(check-answers) → result(Artifact) ───────────────────
@rt("/confirm")
def confirm(sess):
    a = sess.get("answers", {})
    return shell(len(STEPS), Div(
        head("✓", "입력을 확인하세요", "수정해도 다른 답은 그대로 남습니다."),
        Ul(*[Li(Div("✓", cls="pb-ic"),
                Div(Strong(s["title"] + " — "), a.get(s["id"], "-") or "-", "  ",
                    A("수정", href=f"/step/{i}", style="font-size:12px")), cls="pb-okk")
             for i, s in enumerate(STEPS)], cls="pb-gaps"),
        Form(Button("결과 만들기", cls="pb-btn"), action="/result", method="get"), cls="pb-card"))


@rt("/result")
def result(sess):
    a = sess.get("answers", {})
    summary = make_result(a)
    return shell(len(STEPS) + 1, Div(
        head("★", "결과", "결과는 반드시 가져갈 수 있게(Artifact) 끝맺는다."),
        P(summary),
        Form(Button("결과 다운로드 (.txt)", cls="pb-btn"), action="/download", method="get"),
        Div("보조 도구 생성물 — 사용 전 직접 확인하세요.", cls="pb-note"), cls="pb-card"))


@rt("/download")
def download(sess):
    a = sess.get("answers", {})
    txt = "[결과 리포트]\n" + "\n".join(f"- {s['title']}: {a.get(s['id'], '-')}" for s in STEPS) \
          + "\n\n" + make_result(a) + "\n\n※ 보조 도구 생성물."
    return Response(txt, media_type="text/plain; charset=utf-8",
                    headers={"Content-Disposition": 'attachment; filename="result.txt"'})


if __name__ == "__main__":
    serve(port=5025, reload=False)
