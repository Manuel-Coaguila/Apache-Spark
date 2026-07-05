import logging
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from functions.functions import (
    clean_tildes_column,
    clean_numeric_int_column,
    normalize_allowed_values_column,
    normalize_text_column,
)

logger = logging.getLogger("etl.transform")


def run(df: DataFrame) -> DataFrame:
    try:
        logger.debug("Aplicando transformaciones al DataFrame")

        df_transformed = df.select(
            F.current_date().alias("fecha_actual"),
            normalize_text_column(
                "Education",
                invalid_values=["NULL", "null", "None", "none"],
                invalid_value="ERROR",
            ),
            normalize_allowed_values_column("LeaveOrNot", ["0", "1"], invalid_value="ERROR"),
            normalize_text_column(
                "JoiningYear",
                invalid_values=["NULL", "null", "None", "none"],
                invalid_value="ERROR",
            ),
            clean_tildes_column("City"),
            normalize_text_column(
                "PaymentTier",
                invalid_values=["NULL", "null", "None", "none"],
                invalid_value="ERROR",
            ),
            clean_numeric_int_column("Age"),
            normalize_text_column(
                "Gender",
                invalid_values=["NULL", "null", "None", "none"],
                invalid_value="ERROR",
            ),
            normalize_text_column(
                "EverBenched",
                invalid_values=["NULL", "null", "None", "none"],
                invalid_value="ERROR",
            ),
            normalize_text_column(
                "ExperienceInCurrentDomain",
                invalid_values=["NULL", "null", "None", "none"],
                invalid_value="ERROR",
            ),
        )

        logger.info("Transformación aplicada correctamente")
        return df_transformed

    except Exception as exc:
        logger.exception("Error al ejecutar transform.run; %s", exc)
        raise

