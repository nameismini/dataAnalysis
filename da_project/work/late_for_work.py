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
import numpy as np
import re
from datetime import timedelta
from notion_api import NotionDataFetcher
from datetime import datetime

from config import config
from util.common_utils import CommonUtils as util

import holidays

# %% ---------------------------------------
# 엑셀 파일 읽기 (인사팀 매월 초)
# ------------------------------------------

file_path = '../../data/제조서비스팀_0월.xls'
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

# 그룹화
grouped_df = df.groupby(['발생일자', '이름'])['발생시간'].min().reset_index()
result_df = result_df.merge(grouped_df, on=['발생일자', '이름'], how='left')

# 데이터 전처리
result_df['발생일자'] = result_df['발생일자'].apply(util.convert_date_format)
result_df['이름'] = result_df['이름'].apply(util.extract_name)


# 시, 분, 초를 추출하여 새로운 컬럼 추가
result_df[['hours', 'minutes', 'seconds']] = result_df['발생시간'].apply(lambda x: pd.Series(util.parse_time(x)))

# timedelta 객체로 변환하여 새로운 컬럼 추가
result_df['time_delta'] = result_df.apply(
    lambda row: util.time_to_timedelta(row['hours'], row['minutes'], row['seconds']), axis=1)

result_df['발생일자'] = pd.to_datetime(result_df['발생일자'], format='%Y-%m-%d', errors='coerce')
grouped_df['발생일자'] = pd.to_datetime(grouped_df['발생일자'], format='%Y-%m-%d', errors='coerce')

# print("\n변환 및 비교 결과 데이터프레임:", result_df)


# %% ---------------------------------------
# 노션 데이터 가져오기 notion_api.py
# ------------------------------------------

# API 키와 데이터베이스 ID 설정
api_key = config.MFT_NOTION_API_KEY
database_id1 = config.NTDB_ATTENDANCE  # 공유일정
database_id2 = config.NTDB_DAILYCHECK  # 일일점검자

# NotionDataFetcher 인스턴스 생성
fetcher1 = NotionDataFetcher(api_key, database_id1)
fetcher2 = NotionDataFetcher(api_key, database_id2)

# 필요한 컬럼 정의
required_columns1 = ['대상자', '연차차감', '근태구분', '날짜', 'title']
required_columns2 = ['날짜', 'SAP담당자', 'WEB담당자']

# 데이터 가져오기 (시간이 오래걸려서 1회만 api 사용후 나머지는 갱신시에만)
# 시간상 엑셀로 저장된 노션db 가져오기
notion_df1 = fetcher1.get_data_as_dataframe(required_columns1)

# notion_df1.to_excel('notion_df.xlsx', index=False, engine='openpyxl')
# notion_df1 = pd.read_excel('notion_df.xlsx')
notion_df2 = fetcher2.get_data_as_dataframe(required_columns2)

# 근태구분 특문제외
notion_df1['근태구분'] = notion_df1['근태구분'].apply(util.extract_korean)





# %% ---------------------------------------
# 데이터 전처리
# ------------------------------------------
# 1. 노션 데이터 대상자 숫자대로 열로 변경
notion_df1 = notion_df1.assign(대상자=notion_df1['대상자'].str.split(', ')).explode('대상자').reset_index(drop=True)

# 2. 날짜 from ~ to로 공휴일을 제외하고 열로 변경
notion_df1 = util.expand_dates_with_holidays(notion_df1,date_column='날짜')

# '발생일자'와 '날짜'를 datetime 형식으로 변환
notion_df1['날짜'] = pd.to_datetime(notion_df1['날짜'], format='%Y-%m-%d', errors='coerce')
notion_df2['날짜'] = pd.to_datetime(notion_df2['날짜'], format='%Y-%m-%d', errors='coerce')



# %% ---------------------------------------
# 엑셀과 노션데이터 합치기
# ------------------------------------------


# merged_df1 merge 이후 컬럼정리
merged_df1 = pd.merge(result_df, notion_df1, left_on=['발생일자', '이름'], right_on=['날짜', '대상자'], how='left', suffixes=('', '_exl'))  # 병합된 열에 접미사 추가
merged_df1 = merged_df1[['발생일자', '발생시간', '이름', '연차차감', '근태구분','time_delta']].copy()

merged_df2 = pd.merge(merged_df1, notion_df2, left_on=['발생일자', '이름'], right_on=['날짜', 'SAP담당자'], how='left', suffixes=('', '_notion1'))
merged_df2 = merged_df2[['발생일자', '발생시간', '이름', '연차차감', '근태구분','SAP담당자','time_delta']].copy()
# merged_df2.rename(columns={'SAP담당자': 'SAP담당자_SAP'}, inplace=True)

merged_df3 = pd.merge(merged_df2, notion_df2, left_on=['발생일자', '이름'], right_on=['날짜', 'WEB담당자'], how='left', suffixes=('', '_notion2'))
merged_df3 = merged_df3[['발생일자', '발생시간', '이름', '연차차감', '근태구분','SAP담당자','WEB담당자','time_delta']].copy()

# print("Merged DataFrame 열 이름:")
# print('merged_df1 : ',merged_df1.columns)
# print('merged_df2 : ',merged_df2.columns)
# print('merged_df3 : ',merged_df3.columns)

# merged_df3.columns = merged_df3.columns.str.strip()  # 컬럼 이름에서 불필요한 공백 제거

# '일일점검자' 컬럼 추가
merged_df3['일일점검자'] = merged_df3.apply(
    lambda row: 'O' if (row['이름'] == row['SAP담당자'] or row['이름'] == row['WEB담당자']) else 'X',
    axis=1
)

# 소수점 두째자리까지 문자열로 변환
merged_df3['연차차감'] = merged_df3['연차차감'].apply(lambda x: '{:.2f}'.format(x))

# print(merged_df3['근태구분'].unique())

# 연차구분에 따라 출근시간 컬럼 추가
def get_start_time(row):
    if row['근태구분'] == '오전반반차':
        return timedelta(hours=10, minutes=30)  # 연차일 경우 출근시간 08:00
    elif (row['근태구분'] == '오전반차' or row['근태구분'] == '민방위오전'):
        return timedelta(hours=13, minutes=30)  # 연차일 경우 출근시간 08:00
    elif row['일일점검자'] == 'O':
        return timedelta(hours=8, minutes=00)  # 연차일 경우 출근시간 08:00
    else:
        return timedelta(hours=8, minutes=30)  # 일반일 경우 출근시간 08:30

# apply를 사용하여 '출근시간' 컬럼 생성
merged_df3['출근 기준시간'] = merged_df3.apply(get_start_time, axis=1)

# 지각여부를 시, 분 기준으로 비교하여 표기
merged_df3['지각여부'] = merged_df3.apply(
    lambda row: '△' if pd.isna(row['발생시간']) else (
        'O' if pd.notna(row['time_delta']) and (row['time_delta'].seconds // 60) > (row['출근 기준시간'].seconds // 60) else 'X'
    ), axis=1
)

# 불필요 부분 삭제
merged_df3['발생일자'] = merged_df3['발생일자'].dt.strftime('%Y-%m-%d')


# 최종 df
final_df = merged_df3[['발생일자', '발생시간', '이름', '연차차감', '근태구분', '일일점검자', '출근 기준시간', '지각여부']].copy()

# 'A'와 'B' 컬럼을 빈 문자열로 초기화
final_df['지각사유증빙'] = ''
final_df['지각여부 재검증 결과'] = ''

# Timedelta를 "hours:minutes:seconds" 형식의 문자열로 변환
final_df['출근 기준시간'] = final_df['출근 기준시간'].apply(lambda x: str(x).split()[-1])

print(final_df)

# 엑셀 파일로 내보내기
final_df.to_excel('final_df.xlsx', index=False, engine='openpyxl')
