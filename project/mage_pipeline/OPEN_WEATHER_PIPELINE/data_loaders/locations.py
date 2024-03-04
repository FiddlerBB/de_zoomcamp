import io
import pandas as pd
import requests
import json
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

config_path = os.path.join(get_repo_path(), 'io_config.yaml')
config_profile = 'default'

cities = ['An Giang', 'Ba Ria - Vung Tau', 'Bac Lieu', 'Bac Giang', 'Bac Kan', 'Bac Ninh', 
          'Ben Tre', 'Binh Duong', 'Binh Dinh', 'Binh Phuoc', 'Binh Thuan', 'Ca Mau', 'Cao Bang', 
          'Can Tho', 'Da Nang', 'Dak Lak', 'Dak Nong', 'Dien Bien', 'Dong Nai', 'Dong Thap', 'Gia Lai', 
          'Ha Giang', 'Ha Nam', 'Ha Noi', 'Ha Tinh', 'Hai Duong', 'Hai Phong', 'Hau Giang', 'Hoa Binh', 
          'Ho Chi Minh', 'Hung Yen', 'Khanh Hoa', 'Kien Giang', 'Kon Tum', 'Lai Chau', 
          'Lang Son', 'Lao Cai', 'Lam Dong', 'Long An', 'Nam Dinh', 'Nghe An', 'Ninh Binh', 'Ninh Thuan', 
          'Phu Tho', 'Phu Yen', 'Quang Binh', 'Quang Nam', 'Quang Ngai', 'Quang Ninh', 'Quang Tri', 
          'Soc Trang', 'Son La', 'Tay Ninh', 'Thai Binh', 'Thai Nguyen', 'Thanh Hoa', 'Thua Thien Hue', 
          'Tien Giang', 'Tra Vinh', 'Tuyen Quang', 'Vinh Long', 'Vinh Phuc', 'Yen Bai']

def check_table_exist():
    query = 'select * from pelagic-bonbon-387815.de_zoomcamp_pj.locations'
    df = BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)
    
    if df.shape[1] == len(cities):
        print('Table Locations has correct data, getting data from BQ')
        return df
    else:
        print('Getting data for Locations')
        return False

def get_locations():
    locations = []

    for id, city in enumerate(cities):
        print(f'Get data for city: {city}')
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
    Template for loading data from API
    """
    df = check_table_exist()
    if not df:
        df = get_locations()
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert len(output) == len(cities), 'The output is undefined'
