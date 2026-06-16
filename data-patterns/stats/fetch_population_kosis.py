#!/usr/bin/env python
"""KOSIS 주민등록인구 → 시도별 인구·밀도(JSON). (검증된 호출로 실데이터 수신 확인)

원칙: 당일 1회 받아 '고정 데이터'로 저장(실시간 호출 의존 금지).
키: KOSIS(kosis.kr/openapi) — 무료·자동승인. ★ 키 문자열을 그대로(디코드·가공 X) 쓴다.

★ 엔드포인트 주의: 파라미터 방식은 **Param/statisticsParameterData.do**.
  (그냥 statisticsData.do 는 사용자등록(userStatsId) 방식 → '필수변수 누락' err 20 남.)
검증된 표: orgId=101, tblId=DT_1B040A3(행정구역별 성별 인구수), itmId=T20(총인구수),
  objL1=ALL(전국+시도+시군구), objL2 없음, prdSe=Y(연), newEstPrdCnt=N(최근 N기간).

사용:
  python fetch_population_kosis.py --key <KEY> --out population_kosis.json
  python fetch_population_kosis.py --key <KEY> --tbl DT_1B040A3 --itm T20 --years 6 --level sido
"""
import argparse, json, sys, urllib.request, urllib.parse

KOSIS = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
# geo(2018) 시도명 매칭 — KOSIS 최신명 → GeoJSON 이름
NORM = {"강원특별자치도": "강원도", "전북특별자치도": "전라북도"}
SIDO = ["서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시",
        "울산광역시", "세종특별자치시", "경기도", "강원도", "충청북도", "충청남도",
        "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"]


def fetch(params):
    url = KOSIS + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        body = r.read().decode("utf-8")
    j = json.loads(body)
    if isinstance(j, dict) and j.get("err"):
        sys.exit(f"[KOSIS 오류] {j}  (키/표/파라미터 확인)")
    return j


def load_area(path):
    try:
        return {a["name"]: a["area_km2"] for a in json.load(open(path, encoding="utf-8"))}
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="KOSIS apiKey (원문 그대로)")
    ap.add_argument("--tbl", default="DT_1B040A3")
    ap.add_argument("--org", default="101")
    ap.add_argument("--itm", default="T20", help="T20=총인구수")
    ap.add_argument("--years", type=int, default=6, help="최근 N개 연도")
    ap.add_argument("--level", default="sido", choices=["sido", "all"], help="sido=시도만 / all=전체")
    ap.add_argument("--area", default="area_sido.json", help="밀도용 면적 파일")
    ap.add_argument("--out", default="population_kosis.json")
    a = ap.parse_args()

    rows = fetch({"method": "getList", "apiKey": a.key, "format": "json", "jsonVD": "Y",
                  "orgId": a.org, "tblId": a.tbl, "objL1": "ALL", "itmId": a.itm,
                  "prdSe": "Y", "newEstPrdCnt": str(a.years)})

    area = load_area(a.area)
    data, years = {}, set()
    for r in rows:
        nm = NORM.get(r["C1_NM"], r["C1_NM"])
        if a.level == "sido" and nm not in SIDO:
            continue
        years.add(r["PRD_DE"])
        data.setdefault(nm, {})[r["PRD_DE"]] = int(r["DT"])
    years = sorted(years)
    latest = years[-1] if years else None

    keys = SIDO if a.level == "sido" else list(data)
    out = []
    for nm in keys:
        pop = data.get(nm, {}).get(latest)
        km2 = area.get(nm)
        out.append({"region": nm, "population": pop,
                    "density": round(pop / km2) if pop and km2 else None,
                    "area_km2": km2, "by_year": data.get(nm, {})})
    doc = {"_meta": {"source": f"KOSIS {a.tbl}(orgId {a.org}, itm {a.itm})",
                     "years": years, "note": "주민등록인구·당일 수집 고정 데이터. 밀도=인구/면적."},
           "data": out}
    json.dump(doc, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"저장 {len(out)} {a.level} ({years[0]}~{latest}) → {a.out}")


if __name__ == "__main__":
    main()
