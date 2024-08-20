"""
Project Name: dataAnalysis
File Name: __init__.py.py
Author: MKIM
Created Date: 2024-08-07
Description: 
"""
import sys
import os

# 현재 파일 위치 확인
current_directory = os.path.dirname(__file__)
# print(f"Current directory: {current_directory}")

# 상위 디렉터리로 이동 후 'util' 디렉터리 경로를 설정
config_directory = os.path.abspath(os.path.join(current_directory, '..', 'util'))
print(f"Config directory: {config_directory}")
sys.path.append(config_directory)