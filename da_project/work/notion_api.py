"""
Project Name: dataAnalysis
File Name: notion_api.py
Author: Min KIm
Created Date: 2024-08-06
Description: 노션의 근태관리db를 받아옴
"""

# %% import 구간
import requests
import pandas as pd
import json

class NotionDataFetcher:
    def __init__(self, api_key, database_id):
        """
        노션 api 연결

        Parameters:
        api_key (string): api_key
        database_id (string): db id

        Returns:
        self: self init 셋팅
        """
        self.url = f"https://api.notion.com/v1/databases/{database_id}/query"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }

    def fetch_notion_data(self):
        """
        헤더 정보를 통한 노션 api 호출

        Parameters:
        self (self): self에 db url, api key 포함

        Returns:
        list: response 정보 돌려줌
        """
        data = []
        has_more = True
        next_cursor = None

        while has_more:
            payload = {}
            if next_cursor:
                payload['start_cursor'] = next_cursor

            response = requests.post(self.url, headers=self.headers, json=payload)
            # 응답 데이터 처리
            if response.status_code == 200:
                response_data = response.json()
            else:
                print(f"Failed to fetch data: {response.status_code}")
                print(response.json())


            response_data = response.json()

            data.extend(response_data.get('results', []))
            has_more = response_data.get('has_more', False)
            next_cursor = response_data.get('next_cursor', None)

            columns = list(data[0]['properties'].keys())
            # print('columns : ', columns)

            # Creating a dictionary from keys and values
            properties = data[0]['properties']
            first_dict = {key: value for key, value in properties.items()}
            # 딕셔너리를 JSON 문자열로 변환
            # indent=4는 보기 좋게 들여쓰기를 적용하고, ensure_ascii=False는 한글과 같은 비 ASCII 문자를 제대로 표시
            json_string = json.dumps(first_dict, indent=4, ensure_ascii=False)
            print('first_dict (JSON 문자열):', json_string)


        return data

    def parse_notion_response(self, results, required_columns=None):
        """
        노션 테이블 내에서 id를 통한 정보추출

        Parameters:
        results (list): fetch_notion_data에서 추출한 db정보
        required_columns (list): 필요한 컬럼 명시

        Returns:
        dataframe: 필요한 정보만을 추출하여 df로 리턴
        """

        # print('results[0][properties) : ', results[0]['properties'].keys())

        # required_columns이 None이면 모든 컬럼을 포함하는 로직 구현
        if required_columns is not None:
            # required_columns에 있는 컬럼만 포함하는 데이터프레임 반환
            # 실제 구현 내용은 여기에 작성
            pass
        else:
            required_columns             = list(results[0]['properties'].keys())

        columns = {col: [] for col in required_columns}

        for result in results:
            for prop in required_columns:
                prop_value = result['properties'].get(prop, None)
                if prop_value:
                    prop_id = prop_value['id']
                    # 노션테이블의 컬럼 NTDB_ATTENDANCE : 공유일정 테이블
                    if prop_id == '%3F%7DBu':  # 대상자
                        people_value = prop_value.get('people', [])
                        if len(people_value) > 0:  # 리스트가 비어 있지 않으면
                            names = [person.get('name', '') for person in people_value]
                            columns[prop].append(', '.join(names))
                        else:
                            columns[prop].append('')
                    elif prop_id == 'HDJY':  # 연차차감
                        columns[prop].append(prop_value['formula']['number'] if prop_value['formula'] else '')
                    elif prop_id == 'NbP%3F':  # 근태구분
                        columns[prop].append(prop_value['select']['name'] if prop_value['select'] else '')
                    elif prop_id == 'u%7CEP':  # 날짜
                        if prop_value['date']['end']:
                            columns[prop].append(prop_value['date']['start'] + ',' + prop_value['date']['end'])
                        else:
                            columns[prop].append(prop_value['date']['start'] if prop_value['date'] else '')
                    elif prop_id == 'title':  # 이건 컬럼 다 풀고 보면 나옴
                        columns[prop].append(prop_value['title'][0]['text']['content'] if prop_value['title'] else '')
                    # 노션테이블의 컬럼 NTDB_DAILYCHECK : 일일점검 테이블
                    elif prop_id == '%3F%3A%60Q':  # 날짜
                        columns[prop].append(prop_value['date']['start'] if prop_value['date'] else '')
                    elif (prop_id == 'HTTk' or prop_id == 's%7CU_') :  # SAP담당자
                        people_value = prop_value.get('people', [])
                        if len(people_value) > 0:  # 리스트가 비어 있지 않으면
                            names = [person.get('name', '') for person in people_value]
                            columns[prop].append(', '.join(names))
                        else:
                            columns[prop].append('')
                    else:
                        columns[prop].append(None)
                else:
                    columns[prop].append(None)

        return pd.DataFrame(columns)

    def get_data_as_dataframe(self, required_columns=None):
        """
        class 호출용

        Parameters:
        required_columns (list): 필요한 컬럼정보.

        Returns:
        dataframe: parse_notion_response 함수에서 받아온 df
        """
        data = self.fetch_notion_data()
        if required_columns is not None:
              df = self.parse_notion_response(data, required_columns)
        else:
            df = self.parse_notion_response(data)

        return df
