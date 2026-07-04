import logging
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

logger = logging.getLogger("etl.transform")

def run(df: DataFrame) -> DataFrame:
    try:
        logger.debug("Agregando columna fecha_actual")
        ## NO OLVIDAR LIMPIAR ESPACIOS JEJE
        df = df.withColumn("fecha_actual", F.current_date())
        df = df.withColumn("Education", F.when((F.col("Education").isNull()) | (F.col("Education") == ""), "ERROR").otherwise(F.col("Education")))
        df = df.withColumn("LeaveOrNot", F.when(~F.col("LeaveOrNot").isin(["0", "1"]), "ERROR").otherwise(F.col("LeaveOrNot")))

        df_transformed = df.select(
            F.col("Education"),
            F.col("JoiningYear"),
            F.col("City"),
            F.col("PaymentTier"),
            F.col("Age"),
            F.col("Gender"),
            F.col("EverBenched"),
            F.col("ExperienceInCurrentDomain"),
            F.col("LeaveOrNot"),
            F.col("fecha_actual")
        )

        df_transformed.show()
        logger.info("Transformación aplicada correctamente")
    
        return df_transformed

    except Exception as e:
        logger.error("Error al ejecutar transform.run; %s", e, exc_info=True)

        raise 
