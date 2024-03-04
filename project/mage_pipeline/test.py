import pandas as pd

path = r"C:\Users\DELL\Downloads\raw_vietnam_locations.parquet"

df = pd.read_parquet(path)
print(df.head())