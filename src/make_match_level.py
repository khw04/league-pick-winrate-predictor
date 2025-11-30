import pandas as pd
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

# LCK+LPL만 필터해서 만든 CSV
LCK_LPL_PATH = ROOT_DIR / "data" / "processed" / "lck_lpl_matches_champions.csv"
OUT_PATH = ROOT_DIR / "data" / "processed" / "lck_lpl_match_level.csv"


def main():
    print("LCK_LPL_PATH:", LCK_LPL_PATH)
    df = pd.read_csv(LCK_LPL_PATH)
    print("raw LCK_LPL shape:", df.shape)
    print("columns:", list(df.columns)[:20])

    # 1) 선수 행만 사용 (position != 'team')
    if "position" not in df.columns:
        raise ValueError("position 컬럼을 찾을 수 없음")

    df_players = df[df["position"] != "team"].copy()
    print("players rows:", df_players.shape)

    # 필요한 컬럼 이름
    needed = ["gameid", "side", "position", "champion", "result", "teamname"]
    print("\n[컬럼 체크]")
    for c in needed:
        print(c, ":", "OK" if c in df_players.columns else "없음")

    for c in needed:
        if c not in df_players.columns:
            raise ValueError(f"컬럼 없음: {c}  (실제 컬럼명 확인해서 이름 맞춰줘야 함)")

    df_players = df_players[needed].copy()

    # 2) gameid + side 기준으로 포지션별 챔피언 피벗
    pivot = df_players.pivot_table(
        index=["gameid", "side", "teamname"],
        columns="position",
        values="champion",
        aggfunc="first"
    ).reset_index()

    pivot.columns.name = None
    print("pivot shape:", pivot.shape)
    print(pivot.head())

    # 3) 블루 / 레드 분리
    blue = pivot[pivot["side"] == "Blue"].copy()
    red  = pivot[pivot["side"] == "Red"].copy()

    blue = blue.rename(columns={
        "teamname": "blue_team",
        "top": "blue_top_champ",
        "jng": "blue_jungle_champ",
        "mid": "blue_mid_champ",
        "bot": "blue_adc_champ",
        "sup": "blue_support_champ",
    })

    red = red.rename(columns={
        "teamname": "red_team",
        "top": "red_top_champ",
        "jng": "red_jungle_champ",
        "mid": "red_mid_champ",
        "bot": "red_adc_champ",
        "sup": "red_support_champ",
    })

    # 4) 블루팀 승리 여부(result) 붙이기
    results = df_players.drop_duplicates(subset=["gameid", "side"])[["gameid", "side", "result"]]
    blue = blue.merge(
        results[results["side"] == "Blue"][["gameid", "result"]],
        on="gameid",
        how="left"
    )
    blue = blue.rename(columns={"result": "blue_win"})

    # 5) 블루/레드 병합 (경기 단위)
    match_df = blue.merge(
        red[[
            "gameid", "red_team",
            "red_top_champ", "red_jungle_champ", "red_mid_champ",
            "red_adc_champ", "red_support_champ",
        ]],
        on="gameid",
        how="inner"
    )

    match_df = match_df[[
        "gameid",
        "blue_team", "red_team",
        "blue_top_champ", "blue_jungle_champ", "blue_mid_champ",
        "blue_adc_champ", "blue_support_champ",
        "red_top_champ", "red_jungle_champ", "red_mid_champ",
        "red_adc_champ", "red_support_champ",
        "blue_win",
    ]]

    print("match_df shape:", match_df.shape)
    print(match_df.head())

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    match_df.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")
    print("저장 완료:", OUT_PATH)


if __name__ == "__main__":
    main()
