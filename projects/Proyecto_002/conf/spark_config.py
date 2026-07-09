from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv

# /opt/spark/spark-projects/Proyecto_001/conf
# /opt/spark/bin/spark-submit spark_config.py

dotenv_path = '/opt/spark/spark-projects/Proyecto_001/conf/.env.Proyecto_001'
load_dotenv(dotenv_path=dotenv_path)

def get_spark_session():
    try:
        spark = (
            SparkSession.builder
            .appName(os.environ["PROJECT_NAME_P001"])
            .config("spark.jars", os.environ["SQLSERVER_JDBC_JAR_P001"])
            .config("spark.executor.memory", os.environ["SPARK_EXECUTOR_MEMORY_P001"])
            .config("spark.executor.cores", int(os.environ["SPARK_EXECUTOR_CORES_P001"]))
            .config("spark.driver.memory", os.environ["SPARK_DRIVER_MEMORY_P001"])
            .config("spark.driver.cores", int(os.environ["SPARK_DRIVER_CORES_P001"]))
            .getOrCreate()
        )
        print("################################################################")
        print("################################################################")
        print("Spark session created successfully.")
        print("################################################################")
        print("################################################################")
        return spark
    except Exception as e:
        print("########################### ERROR ##############################")
        print("################################################################")
        print(f"Error al crear la sesión de Spark: {e}")
        print("Verifica que las variables de entorno estén configuradas correctamente.")
        print("################################################################")
        print("################################################################")
        raise
