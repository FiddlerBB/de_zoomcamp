-- Question 3
select count(*) from (select lpep_pickup_datetime::date, lpep_dropoff_datetime::date from green_taxi gt
where cast(lpep_pickup_datetime::date as text) = '2019-09-18'
and cast(lpep_dropoff_datetime::date as text) = '2019-09-18') foo

-- Question 4
select * from green_taxi gt 
where trip_distance = (select max(trip_distance) from green_taxi gt )

-- Question 5
select sum(total_amount) total, foo."Borough" from (select cast(gt.lpep_pickup_datetime::date as text) lpep_pickup_datetime, gt.total_amount, z."Borough" from green_taxi gt 
join 
zones z on gt."PULocationID" = z."LocationID" 
where 1=1
and z."Borough" != 'Unknown'
and cast(gt.lpep_pickup_datetime::date as text) = '2019-09-18') foo
group by foo."Borough"
having 1=1
and sum(total_amount)  >= 50000


-- Question 6
with dropoff as (select z2."Zone", sum(gt.tip_amount) tip_amount from green_taxi gt 
join zones z 
on gt."PULocationID" = z."LocationID" 
join zones z2
on gt."DOLocationID" = z."LocationID" 
where z."Zone" = 'Astoria'
group by z2."Zone") 
select * from dropoff
where dropoff.tip_amount = (select max(tip_amount) from dropoff )
