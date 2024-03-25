# Viet Nam air quality

The project get data for 63 major city/town in Viet Nam. And then processing to show the air quality through day.

API usage for this project: 
- [City location](https://nominatim.openstreetmap.org/)
- [Open weather](https://openweathermap.org/api/air-pollution)

## Problems
Viet Nam is facing the with the air pollution these day due to usage of vehicles, transport, production... From the report recently big city usually are covered in mist of dust which contains many harmful gas such as CO, CO2, NO, NO2, S02... So it's useful for us follow the air quality over time

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
Go to [Open weather](https://openweathermap.org) and create a API key
```bash
cd mage_pipeline
echo "OPEN_WEATHER_API_KEY='<your API key>'" >> .env
echo "PROJECT_NAME='<your Mage project name>'" >> .env
echo "DEFAULT_DATE='<your start date you want to get data'" >> .env
echo "BUCKET_NAME='<your bucket name'" >> .env
```




Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)