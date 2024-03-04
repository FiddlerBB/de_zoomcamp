import io
from datetime import datetime
from typing import Union
import time
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
    # df = pd.json_normalize(data, "list", [["coord", "lon"], ["coord", "lat"]])
    # df['city'] = city

    return data


def convert_time_unix(datetime_: Union[datetime, str]) -> int:
    if isinstance(datetime_, str):
        datetime_ = datetime.strptime(datetime_, "%Y-%m-%d")
    unix_time = int(time.mktime(datetime_.timetuple()))
    return unix_time


@data_loader
def load_data_from_api(df: DataFrame, *args, **kwargs):
    """
    Template for loading data from API
    """
    result = []
    start = convert_time_unix("2024-03-01")
    end = convert_time_unix(datetime.now())
    for idx, row in df.head(5).iterrows():
        print(f"getting data from city: {row['city']}")
        metrics = get_pollution_data(start, end, row['latitude'], row['longitude']) 
        metrics['city_id'] = row['city_id']
        result.append(metrics)

    df_result = pd.json_normalize(result, "list", [["coord", "lon"], ["coord", "lat"], 'city_id'])
    return df_result


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'
