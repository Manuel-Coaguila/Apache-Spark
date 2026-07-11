from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from src.config.config import config
import logging

sqlserver_cfg = config["sqlserver"]
paths_cfg = config["paths"]

logger = logging.getLogger("etl.load")


def run(df: DataFrame) -> None:
    try:
        logger.info("Iniciando load.py")
        # Ruta de salida para CSV
        output_csv = f"{paths_cfg['home']}/files/output/Employee_with_date_csv"
        df.write.csv(output_csv, header=True, mode="overwrite")
        print(f"Archivo CSV guardado en: {output_csv}")

        # Ruta de salida para Parquet
        output_parquet = f"{paths_cfg['home']}/files/output/Employee_with_date_parquet"
        df.write.parquet(output_parquet, mode="overwrite")
        print(f"Archivo Parquet guardado en: {output_parquet}")

        # # 🔹 Guardar en SQL Server
        # jdbc_url = f"jdbc:sqlserver://{sqlserver_cfg['host']}:{sqlserver_cfg['port']};databaseName={sqlserver_cfg['database']};encrypt=false;trustServerCertificate=true"
        # connection_properties = {
        #     "user": sqlserver_cfg['username'],
        #     "password": sqlserver_cfg['password'],
        #     "driver": sqlserver_cfg['driver']
        # }

        # (
        #    df.write.
        #    mode("overwrite").
        #    option("batchsize", 1000).
        #    jdbc(url=jdbc_url, table="Employee_with_date", properties=connection_properties)
        # )

        logger.info("DataFrame cargado en tabla SQL Server: Employee_with_date")
        logger.info("ETL finalizado")
        return None
    except Exception as e:
        logger.error("Error en el archivo load.py: %s", e, exc_info=True)
        raise
