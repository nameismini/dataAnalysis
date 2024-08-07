import os
import zipfile
import kaggle as kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

# 닉네임, 토큰 설정
# os.environ["KAGGLE_USERNAME"] = 'ㅇㅇㅇㅇddd'
# os.environ["KAGGLE_KEY"] = "ㅇㅇㅇㅇㅇㅇㅇㅇㅇ"

api = KaggleApi()
api.authenticate()

#파일명은 캐글의 data 아래 부분에 명시되어있음
# api.competition_download_files('house-prices-advanced-regression-techniques')
#
# with zipfile.ZipFile('house-prices-advanced-regression-techniques.zip', 'r') as zipref:
#     zipref.extractall('data/house-prices/')


# import tensorflow_decision_forests as tfdf
import pandas as pd


dataset = pd.read_csv("../../data/house-prices/train.csv")


print(dataset)