if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import io
from datetime import datetime
from typing import Union
import time
import pandas as pd
from pandas import DataFrame
import requests
import os

api_key = os.getenv('OPEN_WEATHER_API_KEY')

def get_pollution_data(start_time: int, end_time: int, lat: float, lon: float, city: str):

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
    df = pd.json_normalize(data, "list", [["coord", "lon"], ["coord", "lat"]])
    df['city'] = city

    return df


def convert_time_unix(datetime_: Union[datetime, str]) -> int:
    if isinstance(datetime_, str):
        datetime_ = datetime.strptime(datetime_, "%Y-%m-%d")
    unix_time = int(time.mktime(datetime_.timetuple()))
    year = datetime_.year
    return unix_time, year

def partition_by_year(df, start_date, end_date):
        


def load_data_from_api(df: DataFrame, *args, **kwargs):
    """
    Template for loading data from API
    """
    start_date = "2024-03-01"
    end_date = datetime.now()
    df_result = pd.DataFrame()
    start, start_year = convert_time_unix(start_date)
    end, end_year = convert_time_unix(end_date)

    for idx, row in df.iterrows():
        for 

        df_city = get_pollution_data(start, end, row['latitude'], row['longitude'], row['city']) 
        df_result = pd.concat([df_result, df_city])
    return df_result
    # return pd.read_csv(io.StringIO(response.text), sep=',')


@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here

    return {}




@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
