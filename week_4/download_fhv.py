import requests
import pandas as pd


link = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/'
'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz'

def download():
    year = 2019
    out_folder = './out/'
    for i in range(12):
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]
        file_name = f"fhv_tripdata_{year}-{month}.csv.gz"
        
        # download it using requests via a pandas df
        request_url = f"{link}{file_name}"
        r = requests.get(request_url)
        open(f'{out_folder}{file_name}', 'wb').write(r.content)
        print(f"Local: {file_name}")

    #     df = pd.read_csv(f'{out_folder}{file_name}', compression='gzip')
    #     final_df = pd.concat([final_df, df])

    # final_df.to_csv(f'{out_folder}fhv_tripdata_{year}.csv', index=False)

# download()
df = pd.DataFrame()
import os
out = './out/'
for file in os.listdir(out):
    df_i = pd.read_csv(out+file, compression='gzip')
    print(f'adding file: {file}')
    df = pd.concat([df, df_i])
df.to_csv('./out/fhv_tripdata_2019.csv', index=False)
