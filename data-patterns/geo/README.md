# geo — 행정경계 기본 자산 (지도 모양)

> **왜 저장?** 행정경계는 거의 안 변한다(시도는 2012 세종시 이후 고정, 시군구만 가끔 통합).
> 한 번 받아 단순화해 두면 **본선 오프라인·반입제약에서도 CDN 없이 지도(choropleth)가 뜬다.**
> 용도: 현황 대시보드(`../../stack/templates/dashboard_app_html.html`)의 지역 분포/밀도 지도.

## 파일
| 파일 | 단위 | 피처 | 크기 | 비고 |
|---|---|---|---|---|
| `skorea-provinces.geojson` | 시도 | 17 | ~186KB | 대시보드 기본 |
| `skorea-municipalities.geojson` | 시군구 | 250 | ~390KB | "우리 동네" 드릴용(시군구 샘플 데이터 필요) |

- 좌표계: WGS84(경위도). 속성: `name`(한글, 예 "서울특별시"/"종로구") · `name_eng` · `code` · `base_year`.
- **ECharts 사용법**: `echarts.registerMap("korea", geojson)` → series `type:"map", map:"korea"`. 데이터 키(REGIONS/SAMPLE_DATA)는 **`properties.name` 과 문자열이 정확히 같아야** 색이 칠해진다.

## 출처 / 라이선스
- 원본: **southkorea/southkorea-maps**(GitHub, e9t/박은정) — 통계청 **SGIS** 행정경계 기반, `base_year=2018`.
- 사용 시 출처 표기 권장(공공 통계 기반 파생). 상업적 사용은 원 저장소 라이선스 확인.

## 재생성 (원본 → 단순화)
원본은 고해상도라 시도 7.5MB·시군구 18MB → `mapshaper`로 단순화해 저장:
```
# 원본 받기
curl -sL -o prov.json  "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea-provinces-2018-geo.json"
curl -sL -o muni.json  "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea-municipalities-2018-geo.json"
# 단순화(폴리곤 간소화 + 좌표 정밀도↓, 작은 섬 보존)
npx -y mapshaper prov.json -simplify 4% keep-shapes -o force precision=0.001 skorea-provinces.geojson
npx -y mapshaper muni.json -simplify 2% keep-shapes -o force precision=0.001 skorea-municipalities.geojson
```
- choropleth 표시용이라 저해상도로 충분(정밀 측정 아님). 더 줄이려면 `-simplify` % 를 낮춘다.
- ⚠️ 시군구는 가끔 바뀐다(예: 2023 군위군 → 대구 편입). 최신성이 중요하면 `base_year` 갱신본으로 교체.
- 실시간 지표(인구·밀도) 데이터는 KOSIS/SGIS에서 → `../how-to-collect.md`(문제정의 근거 출처).
