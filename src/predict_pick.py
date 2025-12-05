import pandas as pd
from pathlib import Path
import joblib

ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT_DIR / "models"
ENCODER_PATH = MODEL_DIR / "pick_encoder.joblib"
MODEL_PATH = MODEL_DIR / "pick_model_logreg.joblib"


def load_model():
    print("모델/인코더 로드 중...")
    encoder = joblib.load(ENCODER_PATH)
    model = joblib.load(MODEL_PATH)
    print("로드 완료.")
    return encoder, model


def build_input_row(
    blue_team, red_team,
    blue_top, blue_jungle, blue_mid, blue_adc, blue_support,
    red_top, red_jungle, red_mid, red_adc, red_support,
):
    data = {
        "blue_team": [blue_team],
        "red_team": [red_team],
        "blue_top_champ": [blue_top],
        "blue_jungle_champ": [blue_jungle],
        "blue_mid_champ": [blue_mid],
        "blue_adc_champ": [blue_adc],
        "blue_support_champ": [blue_support],
        "red_top_champ": [red_top],
        "red_jungle_champ": [red_jungle],
        "red_mid_champ": [red_mid],
        "red_adc_champ": [red_adc],
        "red_support_champ": [red_support],
    }
    return pd.DataFrame(data)


def main():
    encoder, model = load_model()

    print("\n=== 블루/레드 팀 & 챔피언 입력 ===")
    blue_team = input("블루 팀 이름: ")
    red_team = input("레드 팀 이름: ")

    print("\n[블루 챔피언]")
    blue_top = input("  탑: ")
    blue_jungle = input("  정글: ")
    blue_mid = input("  미드: ")
    blue_adc = input("  원딜: ")
    blue_support = input("  서폿: ")

    print("\n[레드 챔피언]")
    red_top = input("  탑: ")
    red_jungle = input("  정글: ")
    red_mid = input("  미드: ")
    red_adc = input("  원딜: ")
    red_support = input("  서폿: ")

    # 1행짜리 입력 DataFrame 생성
    df_input = build_input_row(
        blue_team, red_team,
        blue_top, blue_jungle, blue_mid, blue_adc, blue_support,
        red_top, red_jungle, red_mid, red_adc, red_support,
    )

    # 원-핫 인코딩
    X_encoded = encoder.transform(df_input)

    # 승률 예측 (blue_win=1 확률)
    proba = model.predict_proba(X_encoded)[0, 1]
    print("\n=== 예측 결과 ===")
    print(f"블루 승리 확률: {proba * 100:.2f}%")
    print(f"레드 승리 확률: {(1 - proba) * 100:.2f}%")


if __name__ == "__main__":
    main()
