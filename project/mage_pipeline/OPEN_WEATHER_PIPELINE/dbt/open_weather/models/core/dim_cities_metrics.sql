{{
    config(
        materialized='incremental',
        unique_key=['record_date', 'city_id']
    )
}}

with selected as (select date(TIMESTAMP_SECONDS(dt)) as record_date, aqi, carbon_onoxide_CO, nitric_oxide_NO, nitrogen_ioxide_NO2,
ozone_O3, sulfur_ioxide_SO2, PM2_5, PM10, NH3, city_id
from {{ ref('stg_cities_metrics') }}),

aggerated as (select record_date, city_id, 
round(avg(aqi),2) as avg_aqi, round(avg(carbon_onoxide_CO),2) as avg_CO, round(avg(nitrogen_ioxide_NO2),2) as avg_NO2,
round(avg(ozone_O3), 2) as avg_O3, round(avg(sulfur_ioxide_SO2),2) as avg_SO2, round(avg(PM2_5),2) as avg_PM2_5, round(avg(PM10),2) as avg_PM10
from selected 
group by 1,2)

select * from aggerated


{% if is_incremental() %}

  -- this filter will only be applied on an incremental run
  -- (uses >= to include records whose timestamp occurred since the last run of this model)
  where record_date >= (select max(record_date) from {{ this }})

{% endif %}