# data 디렉토리

이 디렉토리는 LoL 승률 예측 프로젝트에서 사용하는 데이터 파일을 모아둔 곳이다.

## 구조

    data/
    ├─ raw/
    │ └─ 2024_LoL_esports_match_data_from_OraclesElixir.xlsx
    └─ processed/
    │  ├─ lck_lpl_matches_champions.csv
    │  └─ lck_lpl_match_level.csv
    └─ README.md


## raw/

- **2024_LoL_esports_match_data_from_OraclesElixir.xlsx**  
  - 해외 웹사이트에서 다운 받은 원본 경기 데이터. 
  - 직접 수정하지 않고, 참고 / 재생성용으로만 사용한다.

  데이터 출처: https://www.kaggle.com/datasets/barthetur/league-of-legends-2024-competitive-game-dataset

## processed/

- **lck_lpl_matches_champions.csv**  
  - `src/data_preprocess.py`로 생성.  
  - 원본 엑셀에서 리그가 LCK, LPL인 컬럼만 추린 선수/팀 단위 데이터.

- **lck_lpl_match_level.csv**  
  - `src/make_match_level.py`로 생성.  
  - 경기(gameid) 단위로 집계된 데이터.  
  - 팀 이름, 각 포지션 챔피언 10개, `blue_win` 컬럼을 포함하며  
    모델 학습과 UI에서 사용하는 주요 입력 데이터다.