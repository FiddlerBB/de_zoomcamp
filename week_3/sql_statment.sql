create or replace external table `pelagic-bonbon-387815.ny_taxi.external_green_trip_data`
Options(
  format='PARQUET',
  uris=['gs://green_data_2022/green_tripdata_2022.parquet']
);

create or replace table pelagic-bonbon-387815.ny_taxi.green_trip_data as
select * from pelagic-bonbon-387815.ny_taxi.external_green_trip_data
;

select count(distinct(PULocationIDs)) from pelagic-bonbon-387815.ny_taxi.external_green_trip_data;

select count(distinct(PULocationID)) from pelagic-bonbon-387815.ny_taxi.green_trip_data;

select count(*) from pelagic-bonbon-387815.ny_taxi.green_trip_data
where fare_amount=0;

create or replace table pelagic-bonbon-387815.ny_taxi.green_trip_data_partitioned 
partition by date(lpep_pickup_datetime)
cluster by PUlocationID
as
select * from pelagic-bonbon-387815.ny_taxi.external_green_trip_data
;

select count(distinct(PULocationID)) from pelagic-bonbon-387815.ny_taxi.green_trip_data 
where date(lpep_pickup_datetime) between '2022-06-01' and '2022-06-30';

select count(distinct(PULocationID)) from pelagic-bonbon-387815.ny_taxi.green_trip_data_partitioned 
where date(lpep_pickup_datetime) between '2022-06-01' and '2022-06-30'