{{
    config(
        materialized='view'
    )
}}

select dispatching_base_num,
       pickup_datetime,
       dropoff_datetime,
       cast(PULocationID as int) as PULocationID,
       cast(DOLocationID as int) as DOLocationID,
       SR_Flag,
       Affiliated_base_number
from {{ source('staging', 'fhv_tripdata') }}
where extract(year from pickup_datetime) = 2019

-- {% if var('is_test_run', default=true) %}

--   limit 100

-- {% endif %}