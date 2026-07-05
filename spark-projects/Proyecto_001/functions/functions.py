from typing import Iterable, Optional
from pyspark.sql import Column, functions as F

def normalize_text_column(
        column: str,
        invalid_values: Optional[Iterable[str]] = None,
        invalid_value: str = "ERROR",
        remove_accents: bool = False,
) -> Column:
    
    normalized = F.trim(F.col(column))
    normalized = F.regexp_replace(normalized, r'\s+', ' ')

    if remove_accents:
        normalized = F.traslate(normalized,'áéíóúÁÉÍÓÚ','aeiouAEIOU')
    if invalid_values is None:
        return normalized.alias(column)
    
    invalid_condition = (
        normalized.isNull() | (normalized == '') | (normalized.isin(list(invalid_values)))
    )

    return F.when(invalid_condition, invalid_value).otherwise(normalized).alias(column)


def normalize_gender_column(
        column: str,
        invalid_values: Optional[Iterable[str]] = None,
        invalid_value: str = "ERROR",
) -> Column:
    normalized = F.col(column)
    valid_values = ["Female","Male"]
    invalid_condition = (
        ~normalized.isin(list(valid_values))
    )
    return F.when(invalid_condition, invalid_value).otherwise(normalized).alias(column)

def normalize_number_int_positive_column(
        column: str,
        invalid_values: Optional[Iterable[str]] = None,
        invalid_value: int = -1,
) -> Column:
    normalized = F.regexp_replace(F.col(column), r'[^0-9]', '')

    if invalid_values is None:
        return normalized.cast(F.col(column).int()).alias(column)
    invalid_condition = (
        normalized.isNull() | (normalized == '') | (normalized.isin(list(invalid_values)))
    )

    return F.when(invalid_condition, invalid_value).otherwise(normalized.cast(F.col(column).int())).alias(column)