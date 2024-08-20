"""
Project Name: dataAnalysis
File Name: common_utils.py.py
Author: MKIM
Created Date: 2024-08-07
Description: 
"""

import os
import logging
import pandas as pd
import re
import holidays

from datetime import datetime
from datetime import timedelta


class CommonUtils:
    """
    A collection of common utility functions.
    """

    def __init__(self, name):
        self.name = name

    @staticmethod
    def string_to_int(s: str) -> int:
        """
        Converts a string to an integer.

        Parameters:
        s (str): The string to convert.

        Returns:
        int: The converted integer, or None if conversion fails.
        """
        try:
            return int(s)
        except ValueError:
            logging.error(f"Cannot convert {s} to int.")
            return None

    @staticmethod
    def current_datetime_str(format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Returns the current date and time as a string.

        Parameters:
        format (str): The format of the date and time string. Default is "%Y-%m-%d %H:%M:%S".

        Returns:
        str: The formatted date and time string.
        """
        return datetime.datetime.now().strftime(format)

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Reads the content of a file.

        Parameters:
        file_path (str): The path to the file to read.

        Returns:
        str: The content of the file.
        """
        if not os.path.exists(file_path):
            logging.error(f"File {file_path} does not exist.")
            return None
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        Writes content to a file.

        Parameters:
        file_path (str): The path to the file to write to.
        content (str): The content to write to the file.
        """
        with open(file_path, 'w') as file:
            file.write(content)
        logging.info(f"Content written to {file_path}")

    @staticmethod
    def list_files(directory: str) -> list:
        """
        Lists all files in a directory.

        Parameters:
        directory (str): The directory to list files from.

        Returns:
        list: A list of file names in the directory.
        """
        if not os.path.isdir(directory):
            logging.error(f"Directory {directory} does not exist.")
            return []
        return os.listdir(directory)

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
        year = date_str[:4]  # "2024"
        month = date_str[5:7]  # "06"
        day = date_str[8:10]  # "03"

        # 새로운 포맷으로 조합
        new_date_str = f"{year}-{month}-{day}"
        return new_date_str

    def extract_name(text):
        """
        엑셀의 "(" ")" 사이의 이름만 추출

        Parameters:
        a (string): result_df['이름']

        Returns:
        string: 괄호내의 값만 전송
        """
        if pd.isna(text):  # NaN 값 확인
            return None
        match = re.search(r'\((.*?)\)', text)
        if match:
            return match.group(1)
        return text  # 괄호가 없는 경우 None 반환

    def extract_korean(text):
        """
        한글 문자만 추출하기 위한 정규 표현식

        Parameters:
        a (string): 특수문자등 썩여있음

        Returns:
        string: 한글만 리턴
        """
        # 한글 문자만 추출하기 위한 정규 표현식
        if isinstance(text, str):  # text가 문자열인지 확인
            pattern = re.compile(r'[가-힣]+')
            return ''.join(pattern.findall(text))
        else:
            return ''  # 문자열이 아닌 경우 빈 문자열 반환

    def expand_dates_with_holidays(df, date_column):
        """
        주어진 데이터프레임의 날짜 컬럼을 기준으로 주말 및 한국 공휴일을 제외한 날짜들로 행(row)을 확장하는 함수.

        Parameters:
        df (pd.DataFrame): 처리할 데이터프레임
        date_column (str): 날짜가 포함된 컬럼 이름, 기본값은 '날짜'

        Returns:
        pd.DataFrame: 날짜가 확장된 새로운 데이터프레임
        """

        # 한국 공휴일 설정
        kr_holidays = holidays.KR()

        # 결과를 저장할 빈 리스트
        expanded_rows = []

        # DataFrame의 각 행을 순회
        for index, row in df.iterrows():
            # 날짜 형식이 올바른지 확인
            date_str = row[date_column]
            if ',' in date_str:
                try:
                    start_date_str, end_date_str = date_str.split(',')

                    # 문자열을 datetime 객체로 변환
                    start_date = pd.to_datetime(start_date_str)
                    end_date = pd.to_datetime(end_date_str)

                    # 날짜 범위 생성
                    date_range = pd.date_range(start=start_date, end=end_date)

                    # 주말과 공휴일 제외
                    working_days = [date for date in date_range if date not in kr_holidays and date.weekday() < 5]

                    # 각 날짜별로 개별 행(row) 생성
                    for day in working_days:
                        new_row = row.copy()
                        new_row[date_column] = day.strftime('%Y-%m-%d')
                        expanded_rows.append(new_row)
                except Exception as e:
                    print(f"Error processing row {index}: {e}")
            else:
                # 쉼표가 없을 경우 원본 행을 추가
                expanded_rows.append(row)

        # 결과를 새로운 DataFrame으로 변환
        expanded_df = pd.DataFrame(expanded_rows)

        return expanded_df