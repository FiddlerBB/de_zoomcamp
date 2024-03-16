{{ config(materialized='view')}}

select * from {{ source('source', 'locations') }}