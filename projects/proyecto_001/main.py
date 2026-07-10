import logging
import logging.config
import yaml

# Inicializar logging ANTES de cualquier import que use logging
with open("/opt/spark/projects/proyecto_001/conf/logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

from src.spark_sesion.spark_sesion import get_spark_session
from src.etl import extract, transform, load, validation

logger = logging.getLogger("etl.main")

def main():
    try:
        logger.info("####################################################")
        logger.info("####################################################")

        logger.info("Iniciando proceso ETL con Spark")

        spark = get_spark_session()
        logger.info("Sesión Spark inicializada")

        df = extract.run(spark)
        if df is None:
            logger.error("Error en extracción, proceso continuará sin cargar datos")
            return

        df_transformed = transform.run(df)
        if df_transformed is None:
            logger.error("Error en transformación, proceso continuará sin cargar datos")
            return

        df_validation = validation.run(df_transformed)
        if df_validation is None:
            logger.error("Error en validación, proceso continuará sin cargar datos")
            return

        load.run(df_validation)
        logger.info("Datos cargados en destino")

        logger.info("ETL finalizado")

    except Exception as e:
        logger.info("####################################################")
        logger.info("####################################################")
        logger.error("Error crítico en ETL: %s", e, exc_info=True)


if __name__ == "__main__":
    main()