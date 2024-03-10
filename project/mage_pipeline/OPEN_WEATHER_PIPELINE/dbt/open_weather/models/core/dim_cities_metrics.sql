{{
    config(
        materialized='table'
    )
}}

with selected as (select date(TIMESTAMP_SECONDS(dt)) as record_date, aqi, carbon_onoxide_CO, nitric_oxide_NO, nitrogen_ioxide_NO2,
ozone_O3, sulfur_ioxide_SO2, PM2_5, PM10, NH3, city_id
from {{ ref('stg_cities_metrics') }})

select record_date, city_id, 
round(avg(aqi),2) as avg_aqi, round(avg(carbon_onoxide_CO),2) as avg_CO, round(avg(nitrogen_ioxide_NO2),2) as avg_NO2,
round(avg(ozone_O3), 2) as avg_O3, round(avg(sulfur_ioxide_SO2),2) as avg_SO2, round(avg(PM2_5),2) as avg_PM2_5, round(avg(PM10),2) as avg_PM10
from selected 
group by 1,2 