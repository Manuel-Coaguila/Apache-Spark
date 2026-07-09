from pyspark.sql import SparkSession
from src.spark_config.config import config


def get_spark_session():
    try:
        spark_cfg = config["spark"]

        spark = (
            SparkSession.builder
            .appName(spark_cfg["app_name"])
            .config("spark.jars", spark_cfg["jars"])
            .config("spark.executor.memory", spark_cfg["executor_memory"])
            .config("spark.executor.cores", int(spark_cfg["executor_cores"]))
            .config("spark.driver.memory", spark_cfg["driver_memory"])
            .config("spark.driver.cores", int(spark_cfg["driver_cores"]))
            .getOrCreate()
        )
        return spark
    except Exception as e:
        print(f"Error al crear la sesión de Spark: {e}")
        raise