import logging
import os
from pyspark.sql import SparkSession, DataFrame
from schemas.schemas import get_employee_schema

logger = logging.getLogger("etl.extract")

def run(spark: SparkSession) -> DataFrame:
    try:
        logger.info("Cargando archivo")
        path_file = os.getenv("EXTRACT_PATH_FILE_P001")
        if not path_file:
            raise ValueError("Variable de entorno EXTRACT_PATH_FILE_P001 no está definida")

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

