{{
    config(
        materialized='view'
    )
}}

select * from {{ source('staging', 'cities_metrics') }}
limit 10000