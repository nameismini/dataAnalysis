"""
Project Name: dataAnalysis
File Name: __init__.py
Author: MKIM
Created Date: 2024-08-07
Description: 서버에 올릴떄는 필요할지 몰라서 sys.path 를 걸어둠. 파이참에서는 그냥 source 지정으로 path 걸림
"""
import sys
import os

# 현재 파일 위치 확인
current_directory = os.path.dirname(__file__)
print(f"Current directory: {current_directory}")

# 상위 디렉터리로 이동 후 'config' 디렉터리 경로를 설정
config_directory = os.path.abspath(os.path.join(current_directory, '..', 'config'))
print(f"Config directory: {config_directory}")
sys.path.append(config_directory)