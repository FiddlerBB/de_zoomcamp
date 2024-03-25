import io, os, time
from datetime import datetime
from typing import Union
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from mage_ai.io.bigquery import BigQuery

import pandas as pd
from pandas import DataFrame
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

api_key = os.getenv('OPEN_WEATHER_API_KEY')
config_profile = 'default'
bucket_name = 'de_zoomcamp_2024_bucket'
location_object = 'raw/vietnam_locations.parquet'
default_day = os.getenv('DEFAULT_DATE')
config_path = os.path.join(get_repo_path(), 'io_config.yaml')
raw_cities_metrics_table_id = 'pelagic-bonbon-387815.de_zoomcamp_pj.cities_metrics'


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

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )


def get_locations_gcs(object_key) -> DataFrame:
    df = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
    return df


def get_data_bq(query: str):
    try: 
        df = BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)
        return df
    except Exception as e:
        print(e)
        return pd.DataFrame()


def check_cities_metrics_date_bd():
    max_day_query = f'select max(dt) as max_dt from {raw_cities_metrics_table_id} limit 1'
    df = get_data_bq(max_day_query)
    if not df.empty:
        max_day = df.iloc[0]['max_dt']
        print(f'Max day in Bigquery: {max_day}')
    else:
        max_day = None
    return max_day


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    max_day = check_cities_metrics_date_bd()
    
    if max_day:
        start = max_day
    else:
        start = convert_time_unix(default_day)

    print(datetime.utcfromtimestamp(start).strftime('%Y-%m-%d'))

    end = convert_time_unix(datetime.now())

    run_date = datetime.today().strftime('%Y-%m-%d')

    df = get_locations_gcs(location_object)

    objects_path = []
    
    for idx, row in df.iterrows():
        city_name = row['city']
        print(f"getting data from city: {city_name}")

        metrics = get_pollution_data(start, end, row['latitude'], row['longitude']) 
        metrics['city_id'] = row['city_id']

        df = pd.json_normalize(metrics, "list", [["coord", "lon"], ["coord", "lat"], 'city_id'])
        object_name = f'raw/ciy_metrics/{run_date}/{city_name}.parquet'

        export_data_to_google_cloud_storage(df, object_name)
        objects_path.append(object_name)

    return objects_path