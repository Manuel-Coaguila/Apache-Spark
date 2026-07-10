# Guía de JOINs en PySpark - Unión de DataFrames

## ¿Qué es un JOIN en Spark?

Un JOIN en Apache Spark permite combinar registros de dos o más DataFrames basándose en una o más columnas comunes (claves). Es similar a las operaciones JOIN en SQL.

## Tipos de JOINs en PySpark

### 1. **INNER JOIN** (Join Interno)
Devuelve solo los registros que tienen coincidencia en AMBOS DataFrames.

```python
from pyspark.sql import DataFrame

# Sintaxis básica
df_result = df1.join(df2, on="columna_comun", how="inner")

# O usando la versión SQL
df_result = df1.join(df2, on="columna_comun", how="inner")
```

**Ejemplo práctico:**
```python
# Supongamos que tenemos dos DataFrames
# df_employees: Información de empleados
# df_departments: Información de departamentos

# Inner join - Solo empleados que tienen departamento asignado
df_joined = df_employees.join(
    df_departments,
    on="DepartmentID",
    how="inner"
)
```

### 2. **LEFT JOIN** (Join Izquierdo)
Devuelve TODOS los registros del DataFrame izquierdo y los registros coincidentes del derecho. Los no coincidentes del derecho serán NULL.

```python
df_result = df1.join(df2, on="columna_comun", how="left")
```

**Ejemplo práctico:**
```python
# Todos los empleados, incluso si no tienen departamento asignado
df_joined = df_employees.join(
    df_departments,
    on="DepartmentID",
    how="left"
)
```

### 3. **RIGHT JOIN** (Join Derecho)
Devuelve TODOS los registros del DataFrame derecho y los registros coincidentes del izquierdo.

```python
df_result = df1.join(df2, on="columna_comun", how="right")
```

### 4. **FULL OUTER JOIN** (Join Completo)
Devuelve TODOS los registros de ambos DataFrames. Los no coincidentes se completan con NULL.

```python
df_result = df1.join(df2, on="columna_comun", how="outer")
```

### 5. **LEFT SEMI JOIN** (Join Semi-Izquierdo)
Devuelve solo los registros del DataFrame izquierdo que tienen coincidencia en el derecho (similar a INNER pero solo muestra columnas del izquierdo).

```python
df_result = df1.join(df2, on="columna_comun", how="left_semi")
```

### 6. **LEFT ANTI JOIN** (Join Anti-Izquierdo)
Devuelve solo los registros del DataFrame izquierdo que NO tienen coincidencia en el derecho.

```python
df_result = df1.join(df2, on="columna_comun", how="left_anti")
```

## Ejemplos Aplicados a tu Proyecto

### Ejemplo 1: JOIN con múltiples columnas

```python
from pyspark.sql import DataFrame

def join_employees_with_cities(df_employees: DataFrame, df_cities: DataFrame) -> DataFrame:
    """
    Une empleados con información de ciudades usando múltiples columnas
    """
    # JOIN usando múltiples columnas como clave
    df_result = df_employees.join(
        df_cities,
        on=["City", "Country"],  # Múltiples columnas
        how="left"
    )
    return df_result
```

### Ejemplo 2: JOIN con nombres de columnas diferentes

```python
def join_with_different_column_names(df_employees: DataFrame, df_salaries: DataFrame) -> DataFrame:
    """
    JOIN cuando las columnas tienen nombres diferentes en cada DataFrame
    """
    from pyspark.sql.functions import col
    
    df_result = df_employees.join(
        df_salaries,
        on=df_employees["EmployeeID"] == df_salaries["Emp_ID"],  # Columnas con nombres diferentes
        how="inner"
    )
    return df_result
```

### Ejemplo 3: JOIN con selección de columnas específicas

```python
def join_and_select_columns(df_employees: DataFrame, df_departments: DataFrame) -> DataFrame:
    """
    JOIN y selección de columnas específicas del resultado
    """
    df_joined = df_employees.join(
        df_departments,
        on="DepartmentID",
        how="left"
    )
    
    # Seleccionar solo columnas específicas
    df_result = df_joined.select(
        "EmployeeID",
        "Name",
        "Education",
        "DepartmentName",
        "City"
    )
    return df_result
```

### Ejemplo 4: JOIN con renombrado de columnas

```python
from pyspark.sql.functions import col

def join_with_column_rename(df_employees: DataFrame, df_salaries: DataFrame) -> DataFrame:
    """
    JOIN con renombrado de columnas para evitar ambigüedades
    """
    # Renombrar columnas antes del JOIN
    df_salaries_renamed = df_salaries.withColumnRenamed("EmployeeID", "EmpID")
    
    df_result = df_employees.join(
        df_salaries_renamed,
        on=df_employees["EmployeeID"] == df_salaries_renamed["EmpID"],
        how="inner"
    )
    return df_result
```

### Ejemplo 5: Múltiples JOINs encadenados

```python
def multiple_joins(df_employees: DataFrame, 
                   df_departments: DataFrame, 
                   df_locations: DataFrame,
                   df_salaries: DataFrame) -> DataFrame:
    """
    Ejemplo de múltiples JOINs encadenados
    """
    # Primer JOIN: Empleados con Departamentos
    df_step1 = df_employees.join(
        df_departments,
        on="DepartmentID",
        how="left"
    )
    
    # Segundo JOIN: Resultado anterior con Ubicaciones
    df_step2 = df_step1.join(
        df_locations,
        on="LocationID",
        how="left"
    )
    
    # Tercer JOIN: Resultado anterior con Salarios
    df_result = df_step2.join(
        df_salaries,
        on="EmployeeID",
        how="left"
    )
    
    return df_result
```

### Ejemplo 6: JOIN con agregaciones

```python
from pyspark.sql import functions as F

def join_with_aggregation(df_employees: DataFrame, 
                          df_sales: DataFrame) -> DataFrame:
    """
    JOIN con agregación de datos
    """
    # Primero, agregar las ventas por empleado
    df_sales_agg = df_sales.groupBy("EmployeeID").agg(
        F.sum("SaleAmount").alias("TotalSales"),
        F.count("SaleID").alias("NumberOfSales"),
        F.avg("SaleAmount").alias("AverageSale")
    )
    
    # Ahora hacer el JOIN
    df_result = df_employees.join(
        df_sales_agg,
        on="EmployeeID",
        how="left"
    )
    
    # Reemplazar NULL con 0 para empleados sin ventas
    df_result = df_result.fillna({
        "TotalSales": 0,
        "NumberOfSales": 0,
        "AverageSale": 0
    })
    
    return df_result
```

## Aplicación en tu Proyecto

### Ejemplo práctico para tu ETL:

```python
# src/etl/transform.py (extendido)

import logging
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

logger = logging.getLogger("etl.transform")

def join_employees_with_departments(df_employees: DataFrame, 
                                     df_departments: DataFrame) -> DataFrame:
    """
    Une empleados con información de departamentos
    """
    try:
        logger.info("Realizando JOIN entre empleados y departamentos")
        
        df_result = df_employees.join(
            df_departments,
            on="DepartmentID",
            how="left"
        )
        
        logger.info(f"JOIN completado. Registros resultantes: {df_result.count()}")
        return df_result
        
    except Exception as e:
        logger.error(f"Error en JOIN: {e}", exc_info=True)
        raise

def join_with_salary_info(df_employees: DataFrame,
                          df_salaries: DataFrame) -> DataFrame:
    """
    Une empleados con información salarial
    """
    try:
        logger.info("Realizando JOIN con información salarial")
        
        # Calcular estadísticas salariales por empleado
        df_salary_stats = df_salaries.groupBy("EmployeeID").agg(
            F.avg("Salary").alias("AverageSalary"),
            F.max("Salary").alias("MaxSalary"),
            F.min("Salary").alias("MinSalary")
        )
        
        # JOIN
        df_result = df_employees.join(
            df_salary_stats,
            on="EmployeeID",
            how="left"
        )
        
        return df_result
        
    except Exception as e:
        logger.error(f"Error en JOIN salarial: {e}", exc_info=True)
        raise
```

## Mejores Prácticas

### 1. **Broadcast Join para DataFrames pequeños**
```python
from pyspark.sql.functions import broadcast

# Si df_departments es pequeño (< 10 MB), usar broadcast
df_result = df_employees.join(
    broadcast(df_departments),  # Broadcast del DataFrame pequeño
    on="DepartmentID",
    how="left"
)
```

### 2. **Evitar ambigüedades en nombres de columnas**
```python
# Antes del JOIN, renombrar columnas conflictivas
df2_renamed = df2.withColumnRenamed("Name", "DeptName")

df_result = df1.join(df2_renamed, on="ID", how="left")
```

### 3. **Usar columnas de tipo correcto**
```python
# Asegurar que las columnas de JOIN sean del mismo tipo
from pyspark.sql.functions import col

df1 = df1.withColumn("ID", col("ID").cast("integer"))
df2 = df2.withColumn("ID", col("ID").cast("integer"))

df_result = df1.join(df2, on="ID", how="inner")
```

### 4. **Optimizar el orden de JOINs**
```python
# Empezar por el DataFrame más grande
# Aplicar filtros antes del JOIN
df_filtered = df_large.filter(col("Year") == 2024)

df_result = df_filtered.join(df_small, on="ID", how="inner")
```

## Ejemplo Completo Integrado en tu ETL

```python
# src/etl/transform.py

import logging
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

logger = logging.getLogger("etl.transform")

def run_with_joins(spark: SparkSession, 
                   df_employees: DataFrame,
                   df_departments: DataFrame,
                   df_salaries: DataFrame) -> DataFrame:
    """
    Pipeline completo con JOINs
    """
    try:
        logger.info("Iniciando transformaciones con JOINs")
        
        # 1. JOIN con departamentos
        df_step1 = df_employees.join(
            df_departments,
            on="DepartmentID",
            how="left"
        )
        
        # 2. Agregar estadísticas salariales
        df_salary_stats = df_salaries.groupBy("EmployeeID").agg(
            F.avg("Salary").alias("AvgSalary"),
            F.count("*").alias("PaymentCount")
        )
        
        # 3. JOIN con estadísticas salariales
        df_step2 = df_step1.join(
            df_salary_stats,
            on="EmployeeID",
            how="left"
        )
        
        # 4. Seleccionar columnas finales
        df_final = df_step2.select(
            "EmployeeID",
            "Name",
            "Education",
            "DepartmentName",
            "City",
            F.coalesce("AvgSalary", F.lit(0)).alias("AvgSalary"),
            F.coalesce("PaymentCount", F.lit(0)).alias("PaymentCount")
        )
        
        logger.info(f"Transformaciones con JOINs completadas. Registros: {df_final.count()}")
        return df_final
        
    except Exception as e:
        logger.error(f"Error en transformaciones con JOINs: {e}", exc_info=True)
        raise
```

## Resumen de Sintaxis

| Tipo de JOIN | Código PySpark |
|-------------|----------------|
| INNER | `how="inner"` |
| LEFT | `how="left"` |
| RIGHT | `how="right"` |
| FULL OUTER | `how="outer"` |
| LEFT SEMI | `how="left_semi"` |
| LEFT ANTI | `how="left_anti"` |

## Recursos Adicionales

- [Documentación oficial de PySpark JOIN](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.join.html)
- [Optimización de JOINs en Spark](https://spark.apache.org/docs/latest/sql-performance-tuning.html)