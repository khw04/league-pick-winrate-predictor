import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "lck_lpl_match_level.csv"  # 지금 0.59~0.606 나오던 CSV
MODEL_DIR = ROOT_DIR / "models"
ENCODER_PATH = MODEL_DIR / "pick_encoder.joblib"
MODEL_PATH = MODEL_DIR / "pick_model_logreg.joblib"


def main():
    print("DATA_PATH:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    print("data shape:", df.shape)
    print("columns:", list(df.columns))

    # 타깃 / 피처
    y = df["blue_win"]
    feature_cols = [
        "blue_team", "red_team",
        "blue_top_champ", "blue_jungle_champ", "blue_mid_champ",
        "blue_adc_champ", "blue_support_champ",
        "red_top_champ", "red_jungle_champ", "red_mid_champ",
        "red_adc_champ", "red_support_champ",
    ]
    X = df[feature_cols]

    # 원-핫 인코더 학습
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    X_encoded = encoder.fit_transform(X)

    # train / test 분리
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )

    # 로지스틱 회귀 모델 학습
    model = LogisticRegression(
        max_iter=1000,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # 평가
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Test Accuracy: {acc:.3f}")
    print("Confusion matrix:")
    print(cm)

    # 모델/인코더 저장
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(encoder, ENCODER_PATH)
    joblib.dump(model, MODEL_PATH)
    print("저장 완료:")
    print("  encoder ->", ENCODER_PATH)
    print("  model   ->", MODEL_PATH)


if __name__ == "__main__":
    main()
