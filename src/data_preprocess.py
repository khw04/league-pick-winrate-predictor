import pandas as pd
from pathlib import Path

# 이 파일(test.py)이 있는 src 폴더의 부모 = "데과기" 폴더
ROOT_DIR = Path(__file__).resolve().parent.parent

# 원본 / 출력 경로
RAW_PATH = ROOT_DIR / "data" / "raw" / "2024_LoL_esports_match_data_from_OraclesElixir.xlsx"
OUT_PATH = ROOT_DIR / "data" / "processed" / "lck_lpl_matches_champions.csv"

def main():
    print("읽는 중:", RAW_PATH)
    df = pd.read_excel(RAW_PATH)
    print("raw shape:", df.shape)
    print("앞 컬럼들:", list(df.columns)[:20])

    # league 컬럼 이름 확인
    league_col = None
    for c in df.columns:
        if "league" in c.lower():
            league_col = c
            break
    if league_col is None:
        raise ValueError("league 관련 컬럼을 찾지 못함. 실제 컬럼명 한번 확인 필요.")

    print("리그 컬럼:", league_col)

    # LCK, LPL 만 필터
    df_lck_lpl = df[df[league_col].isin(["LCK", "LPL"])].copy()
    print("LCK+LPL shape:", df_lck_lpl.shape)

    # 컬럼/데이터는 그대로 유지한 채로 csv 저장
    df_lck_lpl.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")
    print("저장 완료:", OUT_PATH)

if __name__ == "__main__":
    main()
