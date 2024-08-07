"""
Project Name: dataAnalysis
File Name: late_for_work.py
Author: Min KIm
Created Date: 2024-08-06
Description: 인사팀에서 입출입 정보를 받아와서, 노션의 근태관리와 합쳐서 필요한 정보만 뺴냄
"""


# %% import 구간
# pip install pandas openpyxl

import pandas as pd
import re
from datetime import timedelta
from notion_api import NotionDataFetcher
from datetime import datetime

import sys
import os

from config import config

# %% ---------------------------------------
# 엑셀 파일 읽기 (인사팀 매월 초)
# ------------------------------------------

file_path = '../../data/출입내역.xls'
df = pd.read_excel(file_path)


# 컬럼 이름 변경
df = df.rename(columns={'\'발생일자\'': '발생일자', '\'발생시간\'': '발생시간', '\'이름\'': '이름'})


# '날짜'와 '이름' 열에서 중복 제거
df_unique_names = df['발생일자'].drop_duplicates()
unique_names = df['이름'].unique()


# # 다중 인덱스 생성
multi_index = pd.MultiIndex.from_product([df_unique_names, unique_names], names=['발생일자', '이름'])

# 빈 데이터프레임 생성
result_df = pd.DataFrame(index=multi_index).reset_index()
result_df['최대값'] = None

# 그룹화 및 최대값 계산
grouped_df = df.groupby(['발생일자', '이름'])['발생시간'].min().reset_index()
result_df = result_df.merge(grouped_df, on=['발생일자', '이름'], how='left')


def parse_time(time_str):
    """
    몇시 몇분 몇초 한글을 숫자형태로 변경

    Parameters:
    a (string): "2024년06월03일"

    Returns:
    int: 시, 분, 초를 숫자화
    """
    if isinstance(time_str, str):  # 문자열일 경우에만 처리
        match = re.match(r'(\d+)시(\d+)분(\d+)초', time_str)
        if match:
            hours, minutes, seconds = map(int, match.groups())
            return hours, minutes, seconds
    return None, None, None


# 시, 분, 초를 추출하여 새로운 컬럼 추가
result_df[['hours', 'minutes', 'seconds']] = result_df['발생시간'].apply(lambda x: pd.Series(parse_time(x)))



def time_to_timedelta(hours, minutes, seconds):
    """
    시, 분, 초를 timedelta로 변환하는 함수 정의

    Parameters:
    a (int): 시
    b (int): 분
    a (int): 초

    Returns:
    timedelta: timedelta 형태로 변경
    """
    # NaN 값을 처리
    if pd.isna(hours) or pd.isna(minutes) or pd.isna(seconds):
        return timedelta()
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))


def convert_date_format(date_str):
    """
    일자에 대하여 포맷변경

    Parameters:
    a (string): e.g. "2024년06월03일"

    Returns:
    int: e.g.2024-06-03
    """
    # 날짜 문자열의 포맷 변경
    year = date_str[:4]         # "2024"
    month = date_str[5:7]       # "06"
    day = date_str[8:10]        # "03"

    # 새로운 포맷으로 조합
    new_date_str = f"{year}-{month}-{day}"
    return new_date_str

# 지각시간 설정 (예: 08:00:00)
specific_time = timedelta(hours=8, minutes=30)

# timedelta 객체로 변환하여 새로운 컬럼 추가
result_df['time_delta'] = result_df.apply(lambda row: time_to_timedelta(row['hours'], row['minutes'], row['seconds']),
                                          axis=1)

# 'time_delta' 값과 '발생시간' 열의 존재 여부에 따라 'comparison' 컬럼에 'O', 'X', 또는 '△' 할당
result_df['comparison'] = result_df.apply(
    lambda row: '△' if pd.isna(row['발생시간']) else (
        'O' if pd.notna(row['time_delta']) and row['time_delta'] > specific_time else 'X'
    ), axis=1
)

result_df['발생일자'] = result_df['발생일자'].apply(convert_date_format)
result_df = result_df[['발생일자','이름','발생시간','comparison']]

print("\n변환 및 비교 결과 데이터프레임:", result_df)

# %% ---------------------------------------
# 노션 데이터 가져오기 notion_api.py
# ------------------------------------------

# API 키와 데이터베이스 ID 설정
api_key = {config.MFT_NOTION_API_KEY}
database_id = {config.NTDB_ATTENDANCE}

# NotionDataFetcher 인스턴스 생성
fetcher = NotionDataFetcher(api_key, database_id)

# 필요한 컬럼 정의
required_columns =  ['대상자', '연차차감', '근태구분', '날짜', 'title']

# 데이터 가져오기
notion_df = fetcher.get_data_as_dataframe(required_columns)

# 노션 api 호출
print(notion_df)


# %% ---------------------------------------
# 엑셀과 노션데이터 합치기
# ------------------------------------------

# '발생일자'와 '날짜'로 조인
merged_df = pd.merge(result_df, notion_df, left_on='발생일자', right_on='날짜', how='left')

# '대상자' 컬럼을 콤마로 구분하여 연결
# merged_df['대상자'] = merged_df.groupby('발생일자')['대상자'].transform(lambda x: ','.join(x.dropna().astype(str)))

# 최종 데이터프레임
final_df = merged_df[['발생일자', '이름', '발생시간', 'comparison', '대상자']]


print(final_df)

# 엑셀 파일로 내보내기
# result_df.to_excel('output.xlsx', index=False, engine='openpyxl')
