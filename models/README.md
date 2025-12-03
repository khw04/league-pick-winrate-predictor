# models 디렉토리

이 디렉토리는 LoL 승률 예측 프로젝트에서 학습된 모델 파일을 모아둔 곳이다.  
`src/train_model_pick.py`에서 생성한 결과물을 저장하며, UI와 콘솔 예측에서 공통으로 사용한다.

## 파일 설명

- **pick_encoder.joblib**  
  - OneHotEncoder 객체.  
  - 팀 이름과 챔피언 10개 문자열 피처를 학습 시 사용했던 방식과 동일하게  
    원-핫 인코딩하기 위해 사용한다.
  - `train_model_pick.py` 실행 시 새로 생성/갱신된다.

- **pick_model_logreg.joblib**  
  - 로지스틱 회귀(LogisticRegression) 분류 모델.  
  - 인코딩된 피처를 입력으로 받아 블루 팀의 승리 확률(blue_win)을 예측한다.
  - `train_model_pick.py` 실행 시 학습되어 저장된다.

## 사용 위치

- **콘솔 예측**: `src/predict_pick.py`  
  - 저장된 encoder와 model을 로드해서, 터미널에서 입력한 팀/챔피언 조합의 승률을 예측한다.

- **웹 UI**: `src/streamlit_app.py`  
  - Streamlit 앱에서 encoder와 model을 로드해  
    드롭다운으로 선택한 팀/챔피언 조합에 대한 승률을 보여준다.

## 주의사항

- 이 디렉토리의 파일은 코드에서 자동으로 생성/덮어쓰므로,  
  수동으로 수정하지 않고 **필요하면 `train_model_pick.py`를 다시 실행해서 재생성**한다.
