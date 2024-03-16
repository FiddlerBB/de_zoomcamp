from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

config_path = path.join(get_repo_path(), 'io_config.yaml')
config_profile = 'default'
bucket_name = 'de_zoomcamp_2024_bucket'
table_id = 'pelagic-bonbon-387815.de_zoomcamp_pj.cities_metrics'


def load_from_google_cloud_storage(object_key: str):
    df = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
    df = df.rename(
        columns={
            "components.co": "carbon_onoxide_CO",
            "components.no": "nitric_oxide_NO",
            "components.no2": "nitrogen_ioxide_NO2",
            "components.o3": "ozone_O3",
            "components.so2": "sulfur_ioxide_SO2",
            "components.pm2_5": "PM2_5",
            "components.pm10": "PM10",
            "components.nh3": "NH3",
            "main.aqi": "aqi",
            "coord.lon": 'longitude',
            "coord.lat": 'latitude'
        }
    )
    return df

@data_exporter
def export_data_to_big_query(city_names: list, **kwargs) -> None:
    """
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """
    for file in enumerate(city_names):
        print(file[1])

        df = load_from_google_cloud_storage(f'{file[1]}')
        method = 'append'
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists=method,
        )
