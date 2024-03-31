import pandas as pd
import requests
from pandas import DataFrame
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

cities = ['An Giang', 'Ba Ria - Vung Tau', 'Bac Lieu', 'Bac Giang', 'Bac Kan', 'Bac Ninh', 
          'Ben Tre', 'Binh Duong', 'Binh Dinh', 'Binh Phuoc', 'Binh Thuan', 'Ca Mau', 'Cao Bang', 
          'Can Tho', 'Da Nang', 'Dak Lak', 'Dak Nong', 'Dien Bien', 'Dong Nai', 'Dong Thap', 'Gia Lai', 
          'Ha Giang', 'Ha Nam', 'Ha Noi', 'Ha Tinh', 'Hai Duong', 'Hai Phong', 'Hau Giang', 'Hoa Binh', 
          'Ho Chi Minh', 'Hung Yen', 'Khanh Hoa', 'Kien Giang', 'Kon Tum', 'Lai Chau', 
          'Lang Son', 'Lao Cai', 'Lam Dong', 'Long An', 'Nam Dinh', 'Nghe An', 'Ninh Binh', 'Ninh Thuan', 
          'Phu Tho', 'Phu Yen', 'Quang Binh', 'Quang Nam', 'Quang Ngai', 'Quang Ninh', 'Quang Tri', 
          'Soc Trang', 'Son La', 'Tay Ninh', 'Thai Binh', 'Thai Nguyen', 'Thanh Hoa', 'Thua Thien Hue', 
          'Tien Giang', 'Tra Vinh', 'Tuyen Quang', 'Vinh Long', 'Vinh Phuc', 'Yen Bai']

project_id = os.getenv('PROJECT_ID')
schema = os.getenv('SCHEMA')
table_id = f'{project_id}.{schema}.locations'
config_path = os.path.join(get_repo_path(), 'io_config.yaml')
config_profile = 'default'

def check_table_exist() -> DataFrame:
    '''
    Check raw location table in BQ
    '''
    query = f'select * from {table_id}'
    df = BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)
    if df.shape[0] != len(cities):
        print(f'Table {table_id} has no data or has no correct data. Attempt to get new data')
        return pd.DataFrame()
    else:
        return df

def get_locations() -> DataFrame:
    '''
    Get data from the list and return city long and lat with assigned city_id
    '''
    locations = []

    for id, city in enumerate(cities):
        url = f"https://nominatim.openstreetmap.org/search?q={city},+Vietnam&format=json"
        response = requests.get(url).json()
        location = {
            "city_id": id,
            "latitude": response[0]["lat"],
            "longitude": response[0]["lon"],
            "city": city,
        }
        locations.append(location)
    df = pd.DataFrame.from_records(locations)
    return df


@data_loader
def locations(*args, **kwargs):
    """
    If table is empty then try to get new data
    """
    df = check_table_exist()

    if df.empty:
        df = get_locations()
        return df
    else:
        return None