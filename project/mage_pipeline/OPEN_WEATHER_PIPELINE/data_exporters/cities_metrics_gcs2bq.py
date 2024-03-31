from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
import os
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

config_path = os.path.join(get_repo_path(), 'io_config.yaml')
config_profile = 'default'
bucket_name = os.getenv('BUCKET_NAME')
project_id = os.getenv('PROJECT_ID')
schema = os.getenv('SCHEMA')

table_id = f'{project_id}.{schema}.cities_metrics'


def load_from_google_cloud_storage(object_key: str) -> DataFrame:
    '''
    Load data from bucket and do some small transform to rename column
    '''
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
    Loop through a list of file paths
    Read the file from bucket and export to BQ
    """
    for file in city_names:
        df = load_from_google_cloud_storage(file)
        method = 'append'
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists=method,
        )
