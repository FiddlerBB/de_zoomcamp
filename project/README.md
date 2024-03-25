# Viet Nam air quality

The project get data for 63 major city/town in Viet Nam. And then processing to show the air quality through day.

API usage for this project: 
- [City location](https://nominatim.openstreetmap.org/)
- [Open weather](https://openweathermap.org/api/air-pollution)

## Problems
Viet Nam is facing the with the air pollution these day due to usage of vehicles, transport, production... From the report recently big city usually are covered in mist of dust which contains many harmful gas such as CO, CO2, NO, NO2, S02... So it's useful for us follow the air quality over time.

With Air Quality Index (AQI):
- 1-5: Good-Very Bad
The smaller AQI identify the quality is better, while greater means it's really bad

## Object
Get the data from 63 cities every day and calculate -> Get AQI by each hour -> Get average AQI for each city and build dashboard from this. 
The job will be run on a VM and get data for each day
## Technology

The project uses the following list:
- Cloud: Google Cloud
- Infra: Terraform
- Data Lake: Google Cloud Storage
- Data Warehouse: Google Big Query
- Visualization: Looker
- Orchestration: Mage
- Transformation: DBT

## Flow run
![](https://github.com/FiddlerBB/de_zoomcamp/blob/main/project/image/Screenshot%202024-03-25%20200433.png)
### Location
- The run will try to get location data from list of cities, store the data in GCS and create a raw table in BQ

### Air quality

- Using the information from location it will try to call and get data from Open Weather APi for each cities
- If it's first run it will get data from the default date to today. 
- Else it will compare data from raw cities_metrics table from BQ and get the max datetime from there as start_date and end_date as today.
- The raw files will be store inside the bucket with prefix `raw/cities_metrics/<%Y-%m-%d>/<city_name>.parquet`
- The next step will insert all data from that date to BQ
- From raw table the DBT will insert only newest data, based on datetime. It's reduced loading time when new data appear
- Finally the fact model will combine data from `locations` and `cities_metrics` to final table


## Installation

### 1. Setting GCP
- Go to [GCP](console.cloud.google.com) 
- Create a project with unique name
- Create service account (for easy can set it as a owner)
- Go to the service account you just created -> `Keys` tab -> `Create new key` -> Download the key

### 2. Setting up Infra
- Clone the project
- Copy service key and put it under `project` directory
- Move to `infra` directory
- Run following command to create infra
- `terraform init` -> `terraform plan`
- Check the result it will create 3 objects, a VM, bucket, data warehouse
- If it's what you want you can run `terrafrom apply` to build infra
### 3. Setting project
#### 3.1 Set up Mage
- Go to [Open weather](https://openweathermap.org) and create a API key
- Go to your VM and following this [video](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=14) to set up your VM
- After setting up your VM, ssh to it through VScode and run these command

```bash
cd project/mage_pipeline
echo "OPEN_WEATHER_API_KEY='<your API key>'" >> .env
echo "PROJECT_NAME='<your Mage project name>'" >> .env
echo "DEFAULT_DATE='<your start date you want to get data'" >> .env
echo "BUCKET_NAME='<your bucket name'" >> .env
```

Run docker-compose to build and run
```bash
docker-compose build
docker-compose up -d
```
After it finish, export a port `6789` to local so we can access Mage through 
`http://localhost:6789`
- Go to `<your mage project>`
- Open file `io_config.yaml`  
- Change google credential to `GOOGLE_SERVICE_ACC_KEY_FILEPATH:"/home/src/google_credentials.json"`

#### 3.2 Set up DBT
Since Mage has integrated DBT in it, so we can run DBT within DBT. 
To set up for it simply run `dbt init` and it will create needed component within dbt folder in mage project

Create a new file `<mage_project>/dbt/profiles.yaml`. The file will have a format:
```bash
open_weather:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account-json
      project: pelagic-bonbon-387815
      dataset: de_zoomcamp_pj
      threads: 3 # Must be a value of 1 or greater 
      OPTIONAL_CONFIG: VALUE
      location: US
      
      keyfile_json:
        type:
        project_id:
        private_key_id:
        private_key:
        client_email:
        client_id:
        auth_uri:
        token_uri:
        auth_provider_x509_cert_url:
        client_x509_cert_url:
```
The information in `keyfile_json` is from `GG service account key`, copy value from it and paste it there.

### Usage
Go to [Mage page](http://localhost:6789) -> Pipelines -> Add a trigger -> Run once 
To test the pipeline


[Looker report](https://lookerstudio.google.com/reporting/99987d5e-231e-4286-90a1-d7d503061d53)