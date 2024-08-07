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

class NotionDataFetcher:
    def __init__(self, api_key, database_id):
        """
        Adds two numbers and returns the result.

        Parameters:
        a (int): The first number.
        b (int): The second number.

        Returns:
        int: The sum of the two numbers.
        """
        self.api_key = api_key
        self.database_id = database_id
        self.url = f"https://api.notion.com/v1/databases/{database_id}/query"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def fetch_notion_data(self):
        """
        Adds two numbers and returns the result.

        Parameters:
        a (int): The first number.
        b (int): The second number.

        Returns:
        int: The sum of the two numbers.
        """
        data = []
        has_more = True
        next_cursor = None

        while has_more:
            payload = {}
            if next_cursor:
                payload['start_cursor'] = next_cursor

            response = requests.post(self.url, headers=self.headers, json=payload)
            response_data = response.json()

            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                print(response_data)
                break

            data.extend(response_data.get('results', []))
            has_more = response_data.get('has_more', False)
            next_cursor = response_data.get('next_cursor', None)

        return data

    def parse_notion_response(self, results, required_columns):
        """
        Adds two numbers and returns the result.

        Parameters:
        a (int): The first number.
        b (int): The second number.

        Returns:
        int: The sum of the two numbers.
        """
        columns = {col: [] for col in required_columns}

        for result in results:
            for prop in required_columns:
                prop_value = result['properties'].get(prop, None)
                if prop_value:
                    prop_id = prop_value['id']

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
                        columns[prop].append(prop_value['date']['start'] if prop_value['date'] else '')
                    elif prop_id == 'title':  # 이건 컬럼 다 풀고 보면 나옴
                        columns[prop].append(prop_value['title'][0]['text']['content'] if prop_value['title'] else '')
                    else:
                        columns[prop].append(None)
                else:
                    columns[prop].append(None)

        return pd.DataFrame(columns)

    def get_data_as_dataframe(self, required_columns):
        """
        Adds two numbers and returns the result.

        Parameters:
        a (int): The first number.
        b (int): The second number.

        Returns:
        int: The sum of the two numbers.
        """
        data = self.fetch_notion_data()
        df = self.parse_notion_response(data, required_columns)
        return df
