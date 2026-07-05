"""
functions.py — Funciones puras y componibles de limpieza/validación
para pipelines PySpark sobre datasets masivos (millones de filas,
miles de columnas).
"""

from typing import Iterable, Optional
from pyspark.sql import Column
from pyspark.sql import functions as F

ACCENTS_SOURCE = "áéíóúÁÉÍÓÚ"
ACCENTS_TARGET = "aeiouAEIOU"
DEFAULT_ERROR_SENTINEL = "ERROR"


# ---------- Capa 1: limpieza pura (sin flagging) ----------

def clean_text(expr: Column, strip_accents: bool = False) -> Column:
    """Trim + colapso de espacios múltiples. Castea a string por seguridad."""
    cleaned = F.regexp_replace(F.trim(expr.cast("string")), r"\s+", " ")
    if strip_accents:
        cleaned = F.translate(cleaned, ACCENTS_SOURCE, ACCENTS_TARGET)
    return cleaned


def extract_digits(expr: Column) -> Column:
    """Conserva solo dígitos. NO usar en columnas que puedan tener decimales
    o signo negativo legítimo — para esos casos usar una validación de
    formato con regexp_extract en vez de strip agresivo."""
    return F.regexp_replace(expr, r"[^0-9]", "")


# ---------- Capa 2: flagging (aplicado sobre el resultado ya limpio) ----------

def flag_invalid(
    expr: Column,
    known_invalid_inputs: Optional[Iterable[str]] = None,
    error_sentinel: str = DEFAULT_ERROR_SENTINEL,
) -> Column:
    """Marca como sentinel los valores nulos, vacíos o pertenecientes
    a la lista de entradas conocidas como inválidas."""
    condition = expr.isNull() | (expr == "")
    if known_invalid_inputs:
        condition = condition | expr.isin(list(known_invalid_inputs))
    return F.when(condition, error_sentinel).otherwise(expr)


def flag_outside_domain(
    expr: Column,
    allowed_values: Iterable[str],
    error_sentinel: str = DEFAULT_ERROR_SENTINEL,
) -> Column:
    """Marca como sentinel los valores fuera de un dominio permitido,
    manejando nulos explícitamente (a diferencia del script original)."""
    condition = expr.isNull() | (~expr.isin(list(allowed_values)))
    return F.when(condition, error_sentinel).otherwise(expr)


# ---------- Capa 3: funciones de alto nivel para transform.py ----------

def normalize_text_column(
    column: str,
    known_invalid_inputs: Optional[Iterable[str]] = None,
    error_sentinel: str = DEFAULT_ERROR_SENTINEL,
    strip_accents: bool = False,
) -> Column:
    cleaned = clean_text(F.col(column), strip_accents)
    flagged = flag_invalid(cleaned, known_invalid_inputs, error_sentinel)
    return flagged.alias(column)


def normalize_categorical_column(
    column: str,
    allowed_values: Iterable[str],
    known_invalid_inputs: Optional[Iterable[str]] = None,
    error_sentinel: str = DEFAULT_ERROR_SENTINEL,
    strip_accents: bool = False,
) -> Column:
    """Reemplaza a normalize_gender_column / normalize_status_column,
    unificadas: cualquier columna de dominio cerrado usa esta función."""
    cleaned = clean_text(F.col(column), strip_accents)
    cleaned = flag_invalid(cleaned, known_invalid_inputs, error_sentinel)
    validated = flag_outside_domain(cleaned, allowed_values, error_sentinel)
    return validated.alias(column)


def normalize_positive_int_column(
    column: str,
    known_invalid_inputs: Optional[Iterable[str]] = None,
    error_sentinel: str = DEFAULT_ERROR_SENTINEL,
) -> Column:
    """Corrige los bugs originales: no reaplica flagging después de
    corromper el sentinel, y usa cast('int') correctamente."""
    raw = F.trim(F.col(column).cast("string"))
    invalid_raw = raw.isNull() | (raw == "")
    if known_invalid_inputs:
        invalid_raw = invalid_raw | raw.isin(list(known_invalid_inputs))

    digits_only = extract_digits(raw)
    invalid_after_extraction = digits_only == ""

    is_invalid = invalid_raw | invalid_after_extraction

    return F.when(
        is_invalid, F.lit(error_sentinel)
    ).otherwise(digits_only.cast("int").cast("string")).alias(column)
    # Nota: si la columna final debe quedar como IntegerType real (no string
    # mezclado con "ERROR"), usar la variante con dq_flag separado, ver abajo.