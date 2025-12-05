# src 디렉토리

이 디렉토리는 LoL 승률 예측 프로젝트의 모든 파이썬 소스 코드를 모아둔 곳이다.  
데이터 전처리 → 학습 데이터 생성 → 모델 학습 → 예측/웹 UI 흐름으로 구성된다.

## 파일 설명

- **data_preprocess.py**  
  - `data/raw/2024_LoL_esports_match_data_from_OraclesElixir.xlsx`를 읽어서  
    필요한 컬럼만 정리한 `data/processed/lck_lpl_matches_champions.csv`를 생성한다.  

- **make_match_level.py**  
  - 선수 단위 데이터를 경기(gameid) 단위로 집계해서  
    팀 이름, 각 포지션 챔피언 10개, `blue_win` 정보를 가진  
    `data/processed/lck_lpl_match_level.csv`를 만든다.  

- **train_model_pick.py**  
  - `lck_lpl_match_level.csv`를 사용해  
    팀 이름 + 챔피언 10개 피처로 블루 승리 여부를 예측하는  
    로지스틱 회귀 모델을 학습한다.  
  - 학습된 OneHotEncoder와 모델을 `models/pick_encoder.joblib`,  
    `models/pick_model_logreg.joblib`으로 저장한다.  

- **predict_pick.py**  
  - 콘솔에서 팀/챔피언 10개를 입력받아  
    `models/`에 저장된 encoder와 모델로 블루 승리 확률을 출력한다.  

- **streamlit_app.py**  
  - Streamlit 기반 웹 UI.  
  - 드롭다운으로 팀/챔피언을 선택하면  
    학습된 모델을 사용해 실시간으로 승률을 보여준다.  

## 실행 순서 (일반적인 워크플로우)

1. 데이터/모델이 없을 때 한 번만 실행:
   - `python src/data_preprocess.py`  
   - `python src/match_level.py`  
   - `python src/train_model_pick.py`  

2. 콘솔 예측:
   - `python src/predict_pick.py`  

3. 웹 UI 실행:
   - `streamlit run src/streamlit_app.py`
