import logging
from pyspark.sql import DataFrame
from functions.functions import (
    normalize_text_column,
    normalize_categorical_column,
    normalize_positive_int_column,
)

logger = logging.getLogger("etl.transform")

#Education,JoiningYear,City,PaymentTier,Age,Gender,EverBenched,ExperienceInCurrentDomain,LeaveOrNot

COMMON_INVALID_INPUTS = ["N/A", "Unknown", "Error", "ERROR", "null", "NULL"]

# Configuración declarativa — escalable: agregar columnas es agregar entradas aquí,
# no escribir más código.
TEXT_COLUMNS = ["Education", "City", "EverBenched"]
POSITIVE_INT_COLUMNS = ["JoiningYear", "PaymentTier", "Age", "ExperienceInCurrentDomain"]
CATEGORICAL_COLUMNS = {
    "Gender": ["Female", "Male"],
    "LeaveOrNot": ["1", "0"],
}


def run(df: DataFrame) -> DataFrame:
    try:
        logger.debug(
            "Aplicando transformaciones: %d texto, %d numéricas, %d categóricas",
            len(TEXT_COLUMNS), len(POSITIVE_INT_COLUMNS), len(CATEGORICAL_COLUMNS),
        )

        exprs = []
        exprs += [
            normalize_text_column(c, COMMON_INVALID_INPUTS, strip_accents=True)
            for c in TEXT_COLUMNS
        ]
        exprs += [
            normalize_positive_int_column(c, COMMON_INVALID_INPUTS)
            for c in POSITIVE_INT_COLUMNS
        ]
        exprs += [
            normalize_categorical_column(c, allowed, COMMON_INVALID_INPUTS)
            for c, allowed in CATEGORICAL_COLUMNS.items()
        ]

        df_clean = df.select(*exprs)

        logger.info("Transformación aplicada correctamente sobre %d columnas", len(exprs))
        return df_clean

    except Exception:
        logger.exception("Error al ejecutar transform.run")
        raise