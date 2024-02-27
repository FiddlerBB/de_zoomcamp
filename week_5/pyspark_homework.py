import os
import random
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
# to start spark master and other terminal for worker on window cd $SPARK_HOME/bin
# spark-class.cmd org.apache.spark.deploy.master.Master
# spark-class.cmd org.apache.spark.deploy.worker.Worker <spark_master_url>

fhv_2019_10 = "fhv_tripdata_2019-10.csv.gz"
zone_data = "taxi_zone_lookup.csv"


class SparkProcess:
    def __init__(self) -> None:
        self.spark = self.get_spark_session()
        self.parquet_path = "fhv/2019/10"
        self.fhv_2019_10 = fhv_2019_10
        self.partition_num = 6
        self.download_data()

    @staticmethod
    def get_spark_session() -> SparkSession:
        return SparkSession.builder. \
            master("local[*]"). \
            appName("test"). \
            getOrCreate()
        
    @staticmethod
    def get_fhv_schema():
        return StructType(
            [
                StructField("dispatching_base_num", StringType(), True),
                StructField("pickup_datetime", TimestampType(), True),
                StructField("dropoff_datetime", TimestampType(), True),
                StructField("PULocationID", IntegerType(), True),
                StructField("DOLocationID", IntegerType(), True),
                StructField("SR_Flag", StringType(), True),
                StructField("Affiliated_base_number", StringType(), True),
            ]
        )

    @staticmethod
    def get_zone_schema():
        return StructType(
            [
                StructField("LocationID", IntegerType(), True),
                StructField("Borough", StringType(), True),
                StructField("Zone", StringType(), True),
                StructField("service_zone", StringType(), True),
            ]
        )

    @staticmethod
    def download_data():
        dict_file = {
            fhv_2019_10: "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz",
            zone_data: "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv",
        }
        for key, value in dict_file.items():
            if not os.path.exists(key):
                print(f'Downloading {key}')
                os.system(f"curl -L {value} -o {key}")
            print(f"{key} existed")

    def read_csv(self, path, schema):
        return self.spark.read.option("header", "true").schema(schema).csv(path)

    def write_parquet(self):
        df = self.read_csv(self.fhv_2019_10, self.get_fhv_schema())
        df = df.repartition(self.partition_num)
        df.write.parquet(self.parquet_path, mode="overwrite")

    def read_parquet(self):
        return self.spark.read.parquet(self.parquet_path)


class SparkHW:
    def __init__(self) -> None:
        self.spark = SparkProcess()

    def question_1(self):
        spark_version = self.spark.spark.version
        print(f"Question 1 - Spark version: {spark_version}")
        return spark_version

    def question_2(self):
        self.spark.write_parquet()
        files = [
            file
            for file in os.listdir(self.spark.parquet_path)
            if file.endswith(".parquet")
        ]
        num_file = len(files)
        file_index = random.randint(0, num_file - 1)
        example_file_path = os.path.join(self.spark.parquet_path, files[file_index])
        file_size = os.path.getsize(example_file_path) / (1024 * 1024)
        print(f"Question 2 - Average parquet size: {round(file_size, 0)} MB")
        return file_size

    def question_3(self):
        df_fhv = self.spark.read_parquet()
        df_fhv = df_fhv.withColumn(
            "pickup_date", df_fhv.pickup_datetime.cast(DateType())
        ).withColumn("dropoff_date", F.to_date(df_fhv.dropoff_datetime))
        df_fhv = df_fhv.filter(df_fhv.pickup_date == "2019-10-15")
        rows_count = df_fhv.count()
        print(f"Question 3 - Number of trip on 2019-10-15: {rows_count}")
        return rows_count

    def question_4(self):
        df_fhv = self.spark.read_parquet()
        interval_hour = (
            F.unix_timestamp(df_fhv.dropoff_datetime)
            - F.unix_timestamp(df_fhv.pickup_datetime)
        ) / 3600
        df_fhv = df_fhv.withColumn("trip_time", interval_hour)
        max_trip_time = df_fhv.select(F.max("trip_time")).collect()[0][0]
        print(f"Question 4 - Longest trip time: {max_trip_time} hours")
        return max_trip_time

    def question_6(self):
        df_fhv = self.spark.read_parquet()
        df_zone = self.spark.read_csv(zone_data, self.spark.get_zone_schema()).select(
            "LocationID", "Zone"
        )
        df = df_fhv.join(df_zone, df_fhv.PULocationID == df_zone.LocationID, "inner")
        df_count = df.groupBy("Zone").agg(F.count("*").alias("zone_count"))
        min_count = df_count.orderBy("zone_count").first()["Zone"]
        print(f"Question 6 - The least popular pickup zone: {min_count}")
        return min_count

    def homework(self):
        self.question_1()
        self.question_2()
        self.question_3()
        self.question_4()
        self.question_6()


def main():
    spark = SparkHW()
    spark.homework()


if __name__ == "__main__":
    main()
