{{
    config(
        materialized='view'
    )
}}

with metrics as (
    select *,
    row_number() over(partition by city_id, dt) as rn
    from {{ source('source', 'cities_metrics') }}

)

select dt, aqi,carbon_onoxide_CO,nitric_oxide_NO,nitrogen_ioxide_NO2,
ozone_O3, sulfur_ioxide_SO2, PM2_5, PM10, NH3, longitude, latitude,city_id 

from metrics
where rn = 1
-- limit 10000