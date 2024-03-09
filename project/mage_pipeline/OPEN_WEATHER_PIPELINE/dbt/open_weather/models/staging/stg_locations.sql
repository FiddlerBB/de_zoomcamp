{{ config(materialized='view')}}

select * from {{ source('mage_open_weather', 'open_weather_pipeline_locations_bq') }}