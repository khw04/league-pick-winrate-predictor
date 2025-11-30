import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "lck_lpl_match_level.csv"


def main():
    print("DATA_PATH:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    print("data shape:", df.shape)
    print("columns:", list(df.columns))

    # 타깃(y)와 피처(X) 분리
    y = df["blue_win"]
    feature_cols = [
        "blue_team", "red_team",
        "blue_top_champ", "blue_jungle_champ", "blue_mid_champ",
        "blue_adc_champ", "blue_support_champ",
        "red_top_champ", "red_jungle_champ", "red_mid_champ",
        "red_adc_champ", "red_support_champ",
    ]
    X = df[feature_cols]

    # 원-핫 인코딩
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    X_encoded = encoder.fit_transform(X)

    # train / test 분리
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )

    # 로지스틱 회귀 모델 학습
    model = LogisticRegression(
        max_iter=1000,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # 평가
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Test Accuracy: {acc:.3f}")
    print("Confusion matrix:")
    print(cm)


if __name__ == "__main__":
    main()
