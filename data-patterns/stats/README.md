# stats — 현황 통계 기본 자산 (인구 등)

> 문제정의 근거("왜 문제인가 — 규모·지역성")용 미리 모아둔 현황 통계.
> 지도 모양은 `../geo/`, 이 통계와 합쳐 현황 대시보드(`../../stack/templates/dashboard_app_html.html`)가 숫자를 보여준다.

## 파일
| 파일 | 내용 | 출처 | 비고 |
|---|---|---|---|
| `population_sido.json` | 시도 17 인구 | **Wikidata**(P1082) | **시드** — 키 없이 받음. ⚠️ `ref_date`(기준연월)가 지역마다 다름(정합 스냅샷 아님) |
| `population_kosis.json` | (예정) 정합 최신·시군구·연령 | KOSIS | `fetch_population_kosis.py`로 키 발급 후 생성 |

- `population_sido.json` 의 `sido_geo` = `../geo` 의 2018 시도명과 매칭용(강원특별자치도→강원도, 전북특별자치도→전라북도).

## 정합 최신 받기 (KOSIS) — 권장
1. **키 발급(무료·즉시·자동승인)**: KOSIS `kosis.kr/openapi` 또는 공공데이터포털 `data.go.kr`(통계청_KOSIS 공유서비스, 15059039). 개발계정 1,000/일.
2. **통계표 정하기**: 예) 행정구역(시군구)별 주민등록인구(orgId 101). KOSIS 통계표 페이지 → **"OpenAPI" URL 생성기**로 `tblId·objL·itmId·prdSe` 를 그대로 얻는다(손으로 추측 말 것).
3. **실행**: `python fetch_population_kosis.py --key <KEY> --tbl <tblId> --out population_kosis.json` → 당일 받아 **고정 데이터화**(실시간 호출 금지 원칙).

## 밀도(분모) = 인구 / 면적
- 면적은 `../geo` 의 GeoJSON에서 계산(키 불필요):
  `npx -y mapshaper ../geo/skorea-provinces.geojson -proj EPSG:5179 -each 'area_km2=this.area/1e6' -o area_sido.json` (EPSG:5179=한국 미터좌표 → ㎢).
- 또는 KOSIS/통계청 면적 통계로 교체.

## 대시보드 연결
- `dashboard_app_html.html` 의 `SAMPLE_DATA`(지어낸 샘플)를 이 실데이터로 교체 → 하단 "실제 데이터로 스왑하는 법" 절차. 지역 키는 `sido_geo`(GeoJSON `properties.name`)와 일치시킬 것.

## 한계 / 갱신
- 시드(Wikidata)는 연도 혼재·시도만 — **발표·정합엔 KOSIS 정합 스냅샷 권장.**
- 행정구역은 거의 안 변하나 시군구는 가끔 바뀜(군위 2023 등) — 최신성 필요시 통계표 기준연도 확인.
