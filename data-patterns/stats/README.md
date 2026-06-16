# stats — 현황 통계 기본 자산 (인구 등)

> 문제정의 근거("왜 문제인가 — 규모·지역성")용 미리 모아둔 현황 통계.
> 지도 모양은 `../geo/`, 이 통계와 합쳐 현황 대시보드(`../../stack/templates/dashboard_app_html.html`)가 숫자를 보여준다.

## 파일
| 파일 | 내용 | 출처 | 비고 |
|---|---|---|---|
| `population_kosis.json` | **시도 17 인구·밀도 (2020~2025)** | **KOSIS** DT_1B040A3 | ✅ **정합 실데이터**(주민등록인구·연도별·밀도 포함). 합계 5,111만(2025). 기본으로 이것 사용 |
| `population_sido.json` | 시도 17 인구 | Wikidata(P1082) | 백업 시드(키 없이). ⚠️ `ref_date` 지역마다 다름(정합 아님) — KOSIS본 우선 |
| `area_sido.json` / `area_sgg.json` | 시도17·시군구250 면적(㎢) | GeoJSON 계산 | **밀도 분모**(키 불필요, EPSG:5179) |

- `population_sido.json` 의 `sido_geo` = `../geo` 의 2018 시도명과 매칭용(강원특별자치도→강원도, 전북특별자치도→전라북도).

## KOSIS 데이터 갱신 — 검증된 호출 ✅
`population_kosis.json` 은 아래로 생성됨(2026-06-16, 실수신 확인). 연도확장·갱신 시 재실행:
```
python fetch_population_kosis.py --key <KOSIS키> --years 6 --out population_kosis.json
```
- 키: `kosis.kr/openapi` 무료·자동승인. **키 문자열을 그대로**(base64 디코드 X) 사용.
- ★ 검증된 파라미터: 엔드포인트 **`Param/statisticsParameterData.do`** (그냥 `statisticsData.do`는 사용자등록 방식이라 err20), orgId=`101`, tblId=**`DT_1B040A3`**(행정구역별 성별 인구수), itmId=**`T20`**(총인구수), `objL1=ALL`, **objL2 없음**, `prdSe=Y`, `newEstPrdCnt=N`.
- 시군구/연령까지: `--level all`(시군구 포함) 또는 다른 tblId(예 DT_1B04005N=5세별). 표마다 objL2(연령)·itmId가 다르니 KOSIS 'OpenAPI URL 생성기'로 확인.

## 밀도(분모) = 인구 / 면적
- 면적은 `../geo` 의 GeoJSON에서 계산(키 불필요):
  `npx -y mapshaper ../geo/skorea-provinces.geojson -proj EPSG:5179 -each 'area_km2=this.area/1e6' -o area_sido.json` (EPSG:5179=한국 미터좌표 → ㎢).
- 또는 KOSIS/통계청 면적 통계로 교체.

## 대시보드 연결
- `dashboard_app_html.html` 의 `SAMPLE_DATA`(지어낸 샘플)를 이 실데이터로 교체 → 하단 "실제 데이터로 스왑하는 법" 절차. 지역 키는 `sido_geo`(GeoJSON `properties.name`)와 일치시킬 것.

## 한계 / 갱신
- **기본은 `population_kosis.json`(KOSIS, 정합·연도별·밀도).** Wikidata 시드는 백업(연도 혼재).
- 현재 시도(17)만 — 시군구·연령은 `--level all`/다른 표로 확장 가능(필요 시).
- 행정경계는 거의 안 변하나 시군구는 가끔 바뀜(군위 2023 등) — 최신성 필요시 통계표 기준연도 확인.
