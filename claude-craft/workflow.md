# 작업 루프: Explore → Plan → Implement → Commit

## 4단계
1. **Explore** — 관련 코드·자료 파악 (plan mode로 조사/실행 분리)
2. **Plan** — 접근법 불확실 · 여러 파일 변경 · 낯선 코드일 때 계획
3. **Implement** — 구현 (검증 루프 켜고)
4. **Commit** — 커밋 + 진행 요약

## plan 생략 기준
> **"diff를 한 문장으로 말할 수 있으면 plan 생략."** 작고 명확한 작업은 바로 구현.

## 해커톤 4시간 타임박스
- **0–30분** 문제 분석 + 파이프라인/모듈 매핑 (Explore + Plan)
- **30–90** 데이터 큐레이션 + Context 설계
- **90–180** Implement (검증 루프 ON)
- **180–210** Polish
- **210–240** 발표 준비
- 세션이 끊겨도 **git 커밋 + 진행 파일**로 연속성 유지(새 세션은 기억이 0).

## 출처
- https://code.claude.com/docs/en/best-practices
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
