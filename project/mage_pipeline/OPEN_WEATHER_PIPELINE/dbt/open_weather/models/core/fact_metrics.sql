{{
    config(
        materialized='table'
    )
}}

select locations.city, metrics.* from {{ ref('dim_cities_metrics') }} as metrics
join {{ ref('dim_locations') }} locations 

on metrics.city_id = locations.city_id
