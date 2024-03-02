import requests
from dotenv import load_dotenv
import os
import time
from typing import Union
from datetime import datetime
from pprint import pprint

load_dotenv()

api_key = os.getenv("OPEN_WEATHER_API_KEY")


def get_current_pollution(lat: float, lon: float):
    api_endpoint = "https://api.openweathermap.org/data/2.5/air_pollution"

    response = requests.get(
        api_endpoint,
        params={
            "lat": lat,
            "lon": lon,
            "appid": api_key,
        },
    )

    if response.status_code != 200:
        print("Error: API request failed with status code", response.status_code)
        exit()
    data = response.json()
    pprint(data)

    return data


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
        exit()

    data = response.json()

    return data


def convert_time_unix(datetime_: Union[datetime, str]) -> int:
    if isinstance(datetime_, str):
        datetime_ = datetime.strptime(datetime_, "%Y-%m-%d")
    unix_time = int(time.mktime(datetime_.timetuple()))
    return unix_time


start = convert_time_unix("2024-03-01")
end = convert_time_unix(datetime.now())
hcm_loc = (10.75, 106.66)
pprint(get_pollution_data(start, end, *hcm_loc))
