# LoL 픽 기반 승률 예측기
    컴퓨터공학과 / 
    20233088 권희원, 20253155 하정민
프로 LoL 경기 데이터를 이용해서  
양 팀의 **팀 이름 + 챔피언 10개 픽**을 입력하면 블루 팀 & 레드 팀의 승리 확률을 예측하는 프로젝트다.

## 프로젝트 구조
    Python_project/
    ├─ README.md
    ├─ requirements.txt
    ├─ data/
    │  ├─ raw/
    │  │  └─ 2024_LoL_esports_match_data_from_OraclesElixir.xlsx
    │  ├─ processed/
    │  │  ├─ lck_lpl_matches_champions.csv
    │  │  └─ lck_lpl_match_level.csv
    │  └─ README.md 
    ├─ models/
    │  ├─ pick_encoder.joblib
    │  ├─ pick_model_logreg.joblib
    │  └─ README.md
    └─ src/
        ├─ data_preprocess.py
        ├─ make_match_level.py
        ├─ train_model_pick.py
        ├─ predict_pick.py
        ├─ streamlit_app.py
        └─ README.md


## 주요 파일 설명

- `data_preprocess.py`  
  - OraclesElixir 엑셀(raw 데이터)을 읽어서 `data/processed/lck_lpl_matches_champions.csv`로 저장.

- `make_match_level.py`  
  - 선수 단위 데이터를 경기 단위로 집계해서  
    `data/processed/lck_lpl_match_level.csv`를 생성  
  - 컬럼: gameid, blue_team, red_team, 각 포지션 챔피언 10개, blue_win 등.

- `train_model_pick.py`  
  - `lck_lpl_match_level.csv`를 이용해  
    팀/챔피언 12개 피처 → blue_win 이진 분류 모델을 학습.  
  - 학습된 OneHotEncoder와 모델을 `models/` 폴더에 저장.

- `predict_pick.py`  
  - 콘솔에서 팀/챔피언을 입력하면  
    저장된 encoder/model로 블루 승리 확률을 출력.

- `streamlit_app.py`  
  - 웹 UI.  
  - 드롭다운으로 팀/챔피언을 선택하면 승률을 시각적으로 보여준다.

## 실행 방법

### 1. 환경 설정
`pip install -r requirements.txt`

### 2. 데이터 전처리 (필요할 때만)
    아래 순서로 실행하면 `data/processed/*.csv`와 `models/*.joblib`가 생성된다.
- `python src/data_preprocess.py`
- `python src/make_match_level.py`
- `python src/train_model_pick.py`

### 3. 콘솔에서 예측 테스트
    터미널에 표시되는 안내에 따라 팀/챔피언 이름을 입력하면  
    승리 확률을 확인할 수 있다.
`python src/predict_pick.py`

### 4. Streamlit UI 실행

    터미널에 표시되는 `Local URL (http://localhost:8501 등)`을 브라우저에서 열면  
    팀/챔피언을 선택해서 승률을 확인할 수 있다.
`streamlit run src/streamlit_app.py`
