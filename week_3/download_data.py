import requests
import pandas as pd
import os
import json

link ='https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{}.parquet'
link = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-{}.csv.gz'

def download_files():
    for i in range(1,13):
        i = f'0{str(i)}' if i < 10 else str(i)
        link_i = link.format(i)
        file_name = link_i.split('/')[-1]
        out_file = f'./out/{file_name}'
        r = requests.get(link_i, allow_redirects=True)
        with open(out_file, 'wb') as file:
            file.write(r.content)

def combine_files():
    df = pd.DataFrame()
    for i in range(1, 13):
        i = f'0{str(i)}' if i < 10 else str(i)
        file_name = f'./out/green_tripdata_2022-{i}.parquet'
        df_i = pd.read_parquet(file_name)
        df = pd.concat([df, df_i])
    df.to_parquet('./out/green_tripdata_2022.parquet')

def combine_files():
    df = pd.DataFrame()
    path = './out'
    for file in os.listdir(path):
        if file.endswith('.parquet'):
            df_i = pd.read_parquet(f'{path}/{file}')
            df = pd.concat([df, df_i])
    df.to_parquet('./out/green_tripdata_2022.parquet')

with open('pelagic-bonbon-387815-dd34d6d1c98c.json', 'r') as file:
    cred = json.load(file)

storage = 'green_data_2022'