import logging
from pyspark.sql import SparkSession, DataFrame
from src.schemas.schemas import get_employee_schema
from src.spark_config.config import config

logger = logging.getLogger("etl.extract")
paths_cfg = config["paths"]


def run(spark: SparkSession) -> DataFrame:
    try:
        logger.info("Cargando archivo")
        path_file = paths_cfg["extract_file"]

        schema = get_employee_schema()
        df = (
            spark.read
            .option("header", "true")
            .option("sep", ",")
            .schema(schema)
            .csv(path_file)
        )
        logger.info("Archivo cargado en DataFrame")
        return df

    except Exception as e:
        logger.error("Error al ejecutar extract.run: %s", e, exc_info=True)
        raise