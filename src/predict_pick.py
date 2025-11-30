import streamlit as st
import pandas as pd
from pathlib import Path
import joblib

# 경로 설정
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "_match_level.csv"
MODEL_DIR = ROOT_DIR / "models"
ENCODER_PATH = MODEL_DIR / "pick_encoder.joblib"
MODEL_PATH = MODEL_DIR / "pick_model_logreg.joblib"


@st.cache_resource
def load_model():
    encoder = joblib.load(ENCODER_PATH)
    model = joblib.load(MODEL_PATH)
    return encoder, model


@st.cache_data
def load_options():
    df = pd.read_csv(DATA_PATH)

    # 팀 목록 (blue/red 합쳐서 유니크)
    team_list = sorted(set(df["blue_team"]) | set(df["red_team"]))

    # 챔피언 목록 (10개 컬럼에서 전부 모아서 유니크)
    champ_cols = [
        "blue_top_champ", "blue_jungle_champ", "blue_mid_champ",
        "blue_adc_champ", "blue_support_champ",
        "red_top_champ", "red_jungle_champ", "red_mid_champ",
        "red_adc_champ", "red_support_champ",
    ]
    champs = set()
    for c in champ_cols:
        champs |= set(df[c].dropna())
    champ_list = sorted(champs)

    return team_list, champ_list


def main():
    st.title("LoL 픽 기반 승률 예측기")

    encoder, model = load_model()
    team_list, champ_list = load_options()

    st.subheader("팀 / 챔피언 선택")

    # 팀 선택
    col_team1, col_team2 = st.columns(2)
    with col_team1:
        blue_team = st.selectbox("블루 팀", team_list, key="blue_team")
    with col_team2:
        red_team = st.selectbox("레드 팀", team_list, key="red_team")

    # 챔피언 선택
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 블루 챔피언")
        blue_top = st.selectbox("블루 탑", champ_list, key="b_top")
        blue_jg = st.selectbox("블루 정글", champ_list, key="b_jg")
        blue_mid = st.selectbox("블루 미드", champ_list, key="b_mid")
        blue_adc = st.selectbox("블루 원딜", champ_list, key="b_adc")
        blue_sup = st.selectbox("블루 서폿", champ_list, key="b_sup")

    with col2:
        st.markdown("#### 레드 챔피언")
        red_top = st.selectbox("레드 탑", champ_list, key="r_top")
        red_jg = st.selectbox("레드 정글", champ_list, key="r_jg")
        red_mid = st.selectbox("레드 미드", champ_list, key="r_mid")
        red_adc = st.selectbox("레드 원딜", champ_list, key="r_adc")
        red_sup = st.selectbox("레드 서폿", champ_list, key="r_sup")

    if st.button("승률 예측하기"):
        # 입력 데이터프레임 구성 (train_model_pick.py와 동일한 컬럼 순서)
        df_input = pd.DataFrame({
            "blue_team": [blue_team],
            "red_team": [red_team],
            "blue_top_champ": [blue_top],
            "blue_jungle_champ": [blue_jg],
            "blue_mid_champ": [blue_mid],
            "blue_adc_champ": [blue_adc],
            "blue_support_champ": [blue_sup],
            "red_top_champ": [red_top],
            "red_jungle_champ": [red_jg],
            "red_mid_champ": [red_mid],
            "red_adc_champ": [red_adc],
            "red_support_champ": [red_sup],
        })

        X = encoder.transform(df_input)
        proba = model.predict_proba(X)[0, 1]

        st.subheader("예측 결과")
        st.write(f"블루 승리 확률: {proba * 100:.2f}%")
        st.write(f"레드 승리 확률: {(1 - proba) * 100:.2f}%")


if __name__ == "__main__":
    main()
