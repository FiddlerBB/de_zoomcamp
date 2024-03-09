import io

from datetime import datetime
from typing import Union
import time
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
import pandas as pd
from pandas import DataFrame
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import os

api_key = os.getenv('OPEN_WEATHER_API_KEY')

def get_pollution_data(start_time: int, end_time: int, lat: float, lon: float):

    api_endpoint = "https://api.openweathermap.org/data/2.5/air_pollution/history"

    response = requests.get(
        api_endpoint,
        params={
            "lat": lat,
            "lon": lon,
            "start": start_time,
            "end": end_time,
            "appid": api_key,
        },
    )

    # Check for errors
    if response.status_code != 200:
        print("Error: API request failed with status code", response.status_code)

    data = response.json()
    return data


def convert_time_unix(datetime_: Union[datetime, str]) -> int:
    if isinstance(datetime_, str):
        datetime_ = datetime.strptime(datetime_, "%Y-%m-%d")
    unix_time = int(time.mktime(datetime_.timetuple()))
    return unix_time

def export_data_to_google_cloud_storage(df, object_key) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = os.path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'de_zoomcamp_2024_bucket'
    # object_key = 'raw/vietnam_locations.parquet'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )


@data_loader
def load_data_from_api(df: DataFrame, *args, **kwargs):
    """
    Template for loading data from API
    """
    objects_path = []
    start = convert_time_unix("2023-03-01")
    end = convert_time_unix(datetime.now())
    for idx, row in df.iterrows():
        city_name = row['city']
        print(f"getting data from city: {city_name}")
        metrics = get_pollution_data(start, end, row['latitude'], row['longitude']) 
        metrics['city_id'] = row['city_id']
        df = pd.json_normalize(metrics, "list", [["coord", "lon"], ["coord", "lat"], 'city_id'])
        object_name = f'raw/ciy_metrics/{city_name}.parquet'
        export_data_to_google_cloud_storage(df, object_name)
        objects_path.append(object_name)
    return objects_path
