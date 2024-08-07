"""
Project Name: dataAnalysis
File Name: config.py
Author: MKIM
Created Date: 2024-08-07
Description: 
"""

from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv()

# 전역변수 설정
MFT_NOTION_API_KEY = os.getenv('MFT_NOTION_API_KEY')
NTDB_ATTENDANCE = os.getenv('NTDB_ATTENDANCE')
DATABASE_URL = os.getenv('DATABASE_URL')
DEBUG = os.getenv('DEBUG') == 'True'  # 문자열을 Boolean으로 변환
PORT = int(os.getenv('PORT', 5000))  # 기본값을 설정

# print(f"API Key: {MFT_NOTION_API_KEY}")
# print(f"Database URL: {DATABASE_URL}")
# print(f"Debug mode: {DEBUG}")
# print(f"Port: {PORT}")