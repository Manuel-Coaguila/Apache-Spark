import logging
import logging.config
import yaml

from conf.spark_config import get_spark_session
from etl import extract, transform, load

# Inicializar logging desde logging.yaml
with open("/opt/spark/spark-projects/Proyecto_001/conf/logging.yaml", "r") as f:
    config = yaml.safe_load(f.read()) # Se convierte en diccionario
    logging.config.dictConfig(config)

logger = logging.getLogger("etl.main")

def main():
    try:

        logger.info("####################################################")
        logger.info("####################################################")

        logger.info("Iniciando proceso ETL con Spark")

        spark = get_spark_session()
        logger.info("Sesión Spark inicializada")

        df = extract.run(spark)
        logger.info("Datos extraídos correctamente")

        df_transformed = transform.run(df)
        logger.info("Transformación aplicada")

        load.run(df_transformed)
        logger.info("Datos cargados en destino (CSV, Parquet, SQL Server)")

        logger.info("ETL finalizado con éxito")

    except Exception as e:

        logger.info("####################################################")
        logger.info("####################################################")

        logger.error("Error crítico en ETL: %s", e, exc_info=True)

        raise

if __name__ == "__main__":
    main()
