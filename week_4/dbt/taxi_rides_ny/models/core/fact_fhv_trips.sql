{{
    config(
        materialized='table'
    )
}}

with dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
), 

fhv_data as (
    select * from {{ ref('stg_fhv_tripdata') }}
    where pulocationid is not null
    or dolocationid is not null
)

-- select * from fhv_data limit 10;
select 
fhv_data.dispatching_base_num,
fhv_data.pickup_datetime,
fhv_data.dropoff_datetime,
fhv_data.sr_flag,
fhv_data.affiliated_base_number,
pickup_zones.borough as pickup_borough, pickup_zones.zone as pickup_zone, dropoff_zones.borough as dropoff_borough, dropoff_zones.zone as dropoff_zone
from fhv_data
join dim_zones as pickup_zones
on cast(pulocationid as integer) = pickup_zones.locationid
join dim_zones as dropoff_zones
on cast(dolocationid as integer) = dropoff_zones.locationid