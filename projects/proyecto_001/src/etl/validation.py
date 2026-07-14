from pyspark.sql import DataFrame
from pyspark.sql import functions as F
import logging

logger = logging.getLogger("etl.validation")


def run(df: DataFrame) -> DataFrame | None:
    try:
        # Validar si el DF está vacío
        if df.isEmpty():
            logger.error("El DataFrame está vacío")
            return None

        # Validar duplicados
        total_registros = df.count()
        total_registros_unicos = df.distinct().count()
        if total_registros == total_registros_unicos:
            logger.info("No existen registros duplicados")
        else:
            logger.warning(
                f"Se encontraron {total_registros - total_registros_unicos} duplicados")
            return None

        # Validar nulos y valores inválidos
        null_exprs = [
            F.count(
                F.when(
                    (F.col(c).isNull()) | (F.col(c).isin(
                        "null", "NULL", "NA", "N/A")),
                    c
                )
            ).alias(f"{c}_null")
            for c in df.columns
        ]

        error_exprs = [
            F.count(
                F.when(F.col(c) == "ERROR", c)
            ).alias(f"{c}_error")
            for c in df.columns
        ]

        df_nulls = df.agg(*null_exprs).collect()[0].asDict()
        df_errors = df.agg(*error_exprs).collect()[0].asDict()

        for col_name in df.columns:
            if df_nulls[f"{col_name}_null"] > 0:
                logger.warning(
                    f"Columna {col_name} tiene {df_nulls[f'{col_name}_null']} valores nulos/NA")
                return None
            if df_errors[f"{col_name}_error"] > 0:
                logger.warning(
                    f"Columna {col_name} tiene {df_errors[f'{col_name}_error']} valores ERROR")
                return None

        logger.info("Validaciones completadas: DataFrame válido")
        return df

    except Exception as e:
        logger.error("Error en validation.py: %s", e, exc_info=True)
        raise
