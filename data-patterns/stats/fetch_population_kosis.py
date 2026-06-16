#!/usr/bin/env python
"""KOSIS 인구 통계 → 현황 대시보드용 고정 데이터(JSON).

원칙: 당일 1회 받아 '고정 데이터'로 저장(실시간 호출 의존 금지).
키: KOSIS(kosis.kr/openapi) 또는 공공데이터포털 KOSIS 공유서비스(무료·자동승인).

★ tblId / objL / itmId 는 손으로 추측하지 말고 KOSIS 통계표의 'OpenAPI URL 생성기'에서 그대로 복사.
  예) 행정구역(시군구)별 주민등록인구 = orgId 101. 표마다 코드가 다르다.

사용:
  python fetch_population_kosis.py --key <KEY> --tbl <tblId> --year 2024 --out population_kosis.json
  # 파라미터가 표마다 달라 안 맞으면 --raw 로 응답을 먼저 확인하고 매핑을 맞춘다.
"""
import argparse, json, sys, urllib.request, urllib.parse

KOSIS_URL = "https://kosis.kr/openapi/statisticsData.do"  # 공유서비스 자료조회


def fetch(params):
    url = KOSIS_URL + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="KOSIS apiKey")
    ap.add_argument("--tbl", required=True, help="통계표 tblId (KOSIS OpenAPI 생성기에서 복사)")
    ap.add_argument("--org", default="101", help="기관 orgId (기본 101 통계청)")
    ap.add_argument("--itm", default="T1", help="itmId (표마다 다름)")
    ap.add_argument("--objL1", default="ALL", help="분류1=지역 코드(ALL=전체)")
    ap.add_argument("--prdSe", default="Y", help="주기(Y/M)")
    ap.add_argument("--year", default="2024", help="기준연도(startPrdDe=endPrdDe)")
    ap.add_argument("--out", default="population_kosis.json")
    ap.add_argument("--raw", action="store_true", help="가공 없이 원응답 저장(매핑 확인용)")
    a = ap.parse_args()

    params = {
        "method": "getList", "apiKey": a.key, "format": "json", "jsonVD": "Y",
        "orgId": a.org, "tblId": a.tbl, "itmId": a.itm, "objL1": a.objL1,
        "prdSe": a.prdSe, "startPrdDe": a.year, "endPrdDe": a.year,
    }
    try:
        rows = fetch(params)
    except Exception as e:
        sys.exit(f"[실패] {e}\n→ 키 활성화·tblId·itmId 확인(KOSIS OpenAPI 생성기). --raw 로 응답 점검.")

    if isinstance(rows, dict) and rows.get("err"):
        sys.exit(f"[KOSIS 오류] {rows}\n→ 통계표 OpenAPI 생성기 파라미터로 교체.")

    if a.raw:
        json.dump(rows, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"원응답 {len(rows)}행 → {a.out} (필드 보고 매핑 맞추세요: C1_NM=지역, DT=값, PRD_DE=기간)")
        return

    # 표준 가공: C1_NM(지역) · DT(값) · PRD_DE(기간). 표마다 키가 다르면 --raw 로 확인 후 수정.
    out = []
    for r in rows:
        out.append({
            "region": r.get("C1_NM") or r.get("C2_NM"),
            "value": float(r["DT"]) if r.get("DT") not in (None, "", "-") else None,
            "period": r.get("PRD_DE"), "unit": r.get("UNIT_NM", ""),
            "item": r.get("ITM_NM", ""),
        })
    doc = {"_meta": {"source": "KOSIS", "orgId": a.org, "tblId": a.tbl,
                     "year": a.year, "note": "당일 수집 고정 데이터(실시간 호출 아님)"},
           "data": out}
    json.dump(doc, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"저장 {len(out)}행 → {a.out}")


if __name__ == "__main__":
    main()
