"""
os 임포트
파이썬 내부에서 os에 접근해서 환경변수를 세팅합니다.
파이썬에서 실행했을때 즉효성을 가집니다.
"""
import os
import zipfile
import kaggle as kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

# 닉네임, 토큰 설정
os.environ["KAGGLE_USERNAME"] = 'ㅇㅇㅇㅇddd'
os.environ["KAGGLE_KEY"] = "ㅇㅇㅇㅇㅇㅇㅇㅇㅇ"

api = KaggleApi()
api.authenticate()

print(api.competitions_list())
#파일명은 캐글의 data 아래 부분에 명시되어있음
api.competition_download_files('titanic')

with zipfile.ZipFile('titanic.zip', 'r') as zipref:
    zipref.extractall('data/data_titanic/')