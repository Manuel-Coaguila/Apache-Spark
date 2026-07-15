import logging
import yaml
import logging.config
import os

path_logging = os.getenv("PATH_LOGGING_P001") #or "/opt/spark/projects/proyecto_001/conf/logging.yaml"

with open(path_logging, "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


from src.sesion.sesion import get_spark_session
from src.etl import extract, transform, load, validation

logger = logging.getLogger("etl.main")


def main():
    try:
        logger.info("####################################################")
        logger.info("####################################################")

        logger.info("Iniciando proceso ETL con Spark")

        spark = get_spark_session()

        df = extract.run(spark)
        if df is None:
            spark.stop()
            logger.error(
                "Error en extracción, proceso continuará sin cargar datos")
            return

        df_transformed = transform.run(df)
        if df_transformed is None:
            spark.stop()
            logger.error(
                "Error en transformación, proceso continuará sin cargar datos")
            return

        df_validation = validation.run(df_transformed)
        if df_validation is None:
            spark.stop()
            logger.error(
                "Error en validación, proceso continuará sin cargar datos")
            return

        load.run(df_validation)

        spark.stop()

    except Exception as e:
        logger.info("####################################################")
        logger.info("####################################################")
        logger.error("Error crítico en ETL: %s", e, exc_info=True)
        spark.stop()


if __name__ == "__main__":
    main()
