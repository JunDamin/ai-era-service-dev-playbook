# method/agents-vs-workflows — 워크플로 vs 에이전트 · 병렬화

> 근거: Anthropic(1차). 일부 병렬 패턴은 잠정.

## 단순함부터
- **가장 단순한 해법**(프롬프트 + 평가)부터, 명백히 모자랄 때만 다단계.
- **워크플로** = 정해진 코드 경로로 LLM·도구 오케스트레이션 / **에이전트** = LLM이 스스로 경로·도구 결정.
- 자율성↑ = 비용·오류 누적↑ → **샌드박스·가드레일** 안에서만.

## 병렬화 (속도 — 플레이북 ③기둥)
- 독립 하위작업은 **서브에이전트로 동시 실행**(오케스트레이터-워커). 컨텍스트 분리 + 요약 보고.
- **2인 분업:** A=빌드 드라이빙 / B=데이터·정확성·발표.
- ⚠️ 멀티에이전트는 토큰·비용↑·조율 비용 → **정말 독립적일 때만**.

## 4시간 적용
- 빌드(메인) + 정확성 리뷰·자료 조사(서브에이전트)를 **병렬**로.

## 출처
- https://www.anthropic.com/research/building-effective-agents
- https://www.anthropic.com/engineering/multi-agent-research-system (잠정)
- https://www.anthropic.com/engineering/claude-code-best-practices
