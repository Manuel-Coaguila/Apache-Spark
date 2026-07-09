import logging
from pyspark.sql import DataFrame
from src.functions.functions import (
    normalize_text_column,
    normalize_categorical_column,
    normalize_positive_int_column,
)

logger = logging.getLogger("etl.transform")


COMMON_INVALID_INPUTS = ["N/A", "Unknown", "Error", "ERROR", "null", "NULL"]


TEXT_COLUMNS = ["Education", "City", "EverBenched"]
POSITIVE_INT_COLUMNS = ["JoiningYear", "PaymentTier", "Age", "ExperienceInCurrentDomain"]
CATEGORICAL_COLUMNS = {
    "Gender": ["Female", "Male"],
    "LeaveOrNot": ["1", "0"],
}


def run(df: DataFrame) -> DataFrame:
    try:
        logger.info(
            "Aplicando transformaciones: %d texto, %d numéricas, %d categóricas",
            len(TEXT_COLUMNS), len(POSITIVE_INT_COLUMNS), len(CATEGORICAL_COLUMNS),
        )

        exprs = []

        for col in df.columns:
            if col in TEXT_COLUMNS:
                exprs.append(normalize_text_column(col, COMMON_INVALID_INPUTS, strip_accents=True))
            elif col in POSITIVE_INT_COLUMNS:
                exprs.append(normalize_positive_int_column(col, COMMON_INVALID_INPUTS))
            elif col in CATEGORICAL_COLUMNS:
                allowed = CATEGORICAL_COLUMNS[col]
                exprs.append(normalize_categorical_column(col, allowed, COMMON_INVALID_INPUTS))
            else:
                logger.warning("Columna %s no está configurada para normalización", col)


        df_clean = df.select(*exprs)

        logger.info("Transformación aplicada correctamente sobre %d columnas", len(exprs))
        return df_clean

    except Exception:
        logger.exception("Error al ejecutar transform.run")
        raise