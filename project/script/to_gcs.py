from google.cloud import storage
import os

'''
Flow
download 2 files -> gcs -> process the file in dataframe -> bigquery -> dbt/spark? -> dashboard

tools:
- mage
- docker
- dbt
- spark
- gcs/gcp
'''

bucket_name = 'de_zoomcamp_2024_bucket'
object_name = "raw/vietnam_locations.json"
local_file = "./script/vietnam_locations.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"

def upload_to_gcs(bucket_name, object_name, local_file):
    """Upload a file to a GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)
    print(f"File {local_file} uploaded to {bucket_name}/{object_name}")


