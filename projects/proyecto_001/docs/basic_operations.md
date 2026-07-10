# Guía de Operaciones Básicas con DataFrames en PySpark

## 1. Detectar Valores Nulos (NULL)

### 1.1 Verificar si una columna es NULL

```python
from pyspark.sql.functions import col, isnan, when, count, lit

# Método 1: Usando isNull() - Para valores NULL
df.filter(col("City").isNull()).show()

# Método 2: Usando isnan() - Para valores NaN (numéricos)
df.filter(col("Salary").isNaN()).show()

# Método 3: Ambos NULL y NaN
df.filter(col("City").isNull() | isnan(col("Salary"))).show()
```

### 1.2 Contar nulos por columna

```python
from pyspark.sql.functions import col, sum as spark_sum, when, count

# Contar nulos en columnas específicas
def count_nulls(df):
    """
    Cuenta valores nulos por cada columna del DataFrame
    """
    null_counts = []
    for column in df.columns:
        null_count = df.filter(
            col(column).isNull() | isnan(col(column))
        ).count()
        null_counts.append((column, null_count))
    
    return null_counts

# Uso
nulls = count_nulls(df)
for col_name, count in nulls:
    print(f"{col_name}: {count} nulos")
```

### 1.3 Contar nulos de forma más eficiente

```python
from pyspark.sql.functions import col, sum as spark_sum, when

# Método eficiente usando agg
def count_nulls_efficient(df):
    """
    Cuenta nulos de forma eficiente para todas las columnas
    """
    exprs = []
    for column in df.columns:
        exprs.append(
            count(when(col(column).isNull(), column)).alias(f"{column}_nulls")
        )
    
    return df.agg(*exprs)

# Uso
null_counts_df = count_nulls_efficient(df)
null_counts_df.show()
```

### 1.4 Porcentaje de nulos por columna

```python
from pyspark.sql.functions import col, count, when, round

def null_percentage(df):
    """
    Calcula el porcentaje de nulos por columna
    """
    total_rows = df.count()
    exprs = []
    
    for column in df.columns:
        null_count = count(when(col(column).isNull(), column)).alias(f"{column}_nulls")
        null_pct = round(
            (count(when(col(column).isNull(), column)) / total_rows) * 100,
            2
        ).alias(f"{column}_null_pct")
        exprs.extend([null_count, null_pct])
    
    return df.agg(*exprs)

# Uso
null_stats = null_percentage(df)
null_stats.show()
```

## 2. Contar Registros

### 2.1 Contar todos los registros

```python
# Contar todos los registros (acción - ejecuta el job)
total = df.count()
print(f"Total de registros: {total}")
```

### 2.2 Contar registros por grupo

```python
from pyspark.sql.functions import count

# Contar por una columna
df.groupBy("City").count().show()

# Contar por múltiples columnas
df.groupBy("City", "Education").count().show()
```

### 2.3 Contar registros distintos

```python
from pyspark.sql.functions import countDistinct

# Contar valores únicos en una columna
df.select(countDistinct("City").alias("unique_cities")).show()

# Contar valores únicos en múltiples columnas
df.select(
    countDistinct("City").alias("unique_cities"),
    countDistinct("Education").alias("unique_education")
).show()
```

### 2.4 Contar con condiciones

```python
from pyspark.sql.functions import count, when

# Contar registros que cumplen una condición
df.select(
    count("*").alias("total"),
    count(when(col("Age") > 30, True)).alias("over_30"),
    count(when(col("Gender") == "Female", True)).alias("females")
).show()
```

## 3. Filtrar Datos

### 3.1 Filtrar con condiciones simples

```python
# Método 1: filter()
df.filter(col("Age") > 30).show()
df.filter("Age > 30").show()  # Usando SQL string

# Método 2: where() - equivalente a filter()
df.where(col("City") == "Bangalore").show()
```

### 3.2 Filtrar con múltiples condiciones

```python
from pyspark.sql.functions import col

# AND - ambas condiciones deben cumplirse
df.filter(
    (col("Age") > 30) & (col("City") == "Bangalore")
).show()

# OR - al menos una condición
df.filter(
    (col("City") == "Bangalore") | (col("City") == "Pune")
).show()

# NOT - negación
df.filter(~(col("City") == "Bangalore")).show()
df.filter(col("City") != "Bangalore").show()
```

### 3.3 Filtrar con IN

```python
# Filtrar por lista de valores
df.filter(
    col("City").isin("Bangalore", "Pune", "New Delhi")
).show()

# Negado - valores que NO están en la lista
df.filter(
    ~col("City").isin("Bangalore", "Pune")
).show()
```

### 3.4 Filtrar con LIKE (patrones)

```python
# Contiene
df.filter(col("City").like("%Bangalore%")).show()

# Empieza con
df.filter(col("City").like("Bang%")).show()

# Termina con
df.filter(col("City").like("%ore")).show()
```

### 3.5 Filtrar con between

```python
# Rango de valores
df.filter(col("Age").between(25, 35)).show()
```

## 4. Seleccionar Columnas

### 4.1 Seleccionar columnas específicas

```python
# Seleccionar columnas específicas
df.select("Name", "City", "Age").show()

# Múltiples columnas como lista
columns = ["Name", "City", "Age", "Education"]
df.select(*columns).show()
```

### 4.2 Seleccionar con alias

```python
from pyspark.sql.functions import col

# Renombrar columnas en la selección
df.select(
    col("Name").alias("EmployeeName"),
    col("City").alias("Location"),
    col("Age").alias("EmployeeAge")
).show()
```

### 4.3 Seleccionar con expresiones

```python
from pyspark.sql.functions import concat, lit

# Crear nuevas columnas en la selección
df.select(
    "Name",
    "City",
    concat(col("Name"), lit(" - "), col("City")).alias("Name_City")
).show()
```

## 5. Ordenar Datos

### 5.1 Ordenar por una columna

```python
from pyspark.sql.functions import col

# Ascendente (por defecto)
df.orderBy("Age").show()

# Descendente
df.orderBy(col("Age").desc()).show()
df.orderBy("Age", ascending=False).show()
```

### 5.2 Ordenar por múltiples columnas

```python
# Ordenar por City ascendente y Age descendente
df.orderBy(col("City").asc(), col("Age").desc()).show()
```

### 5.3 Ordenar con nulls primero/último

```python
# Nulls al final
df.orderBy(col("City").asc_nulls_last()).show()

# Nulls al principio
df.orderBy(col("City").desc_nulls_first()).show()
```

## 6. Eliminar Duplicados

### 6.1 Eliminar filas duplicadas completamente

```python
# Eliminar filas duplicadas (todas las columnas iguales)
df_distinct = df.distinct()
df_distinct.show()
```

### 6.2 Eliminar duplicados por columnas específicas

```python
# Eliminar duplicados basados en columnas específicas
df.dropDuplicates(["City", "Education"]).show()

# Mantener la primera ocurrencia
df.dropDuplicates(["EmployeeID"]).show()
```

## 7. Agregaciones Básicas

### 7.1 Funciones de agregación comunes

```python
from pyspark.sql.functions import count, sum, avg, min, max, stddev

# Agregaciones básicas
df.select(
    count("*").alias("total_records"),
    sum("Salary").alias("total_salary"),
    avg("Age").alias("avg_age"),
    min("Age").alias("min_age"),
    max("Age").alias("max_age"),
    stddev("Salary").alias("std_salary")
).show()
```

### 7.2 Agregaciones por grupo

```python
from pyspark.sql.functions import count, avg, sum

# Agregación por una columna
df.groupBy("City").agg(
    count("*").alias("employee_count"),
    avg("Age").alias("avg_age"),
    avg("Salary").alias("avg_salary")
).show()

# Agregación por múltiples columnas
df.groupBy("City", "Education").agg(
    count("*").alias("count"),
    avg("Age").alias("avg_age")
).show()
```

### 7.3 Agregaciones con alias

```python
from pyspark.sql.functions import count, avg, sum

# Usar alias para claridad
df.groupBy("City").agg(
    count("*").alias("total_employees"),
    avg("Salary").alias("average_salary"),
    sum("Salary").alias("total_salary_budget")
).show()
```

## 8. Manejo de Valores Nulos

### 8.1 Eliminar filas con nulos

```python
from pyspark.sql.functions import col

# Eliminar cualquier fila que tenga al menos un nulo
df.dropna().show()

# Eliminar filas donde columnas específicas sean nulas
df.dropna(subset=["City", "Age"]).show()

# Eliminar con umbral (al menos X columnas no nulas)
df.dropna(thresh=5).show()  # Al menos 5 columnas no nulas
```

### 8.2 Rellenar valores nulos

```python
from pyspark.sql.functions import col, lit

# Rellenar todos los nulos con un valor específico
df.fillna(0).show()  # Todos los nulos se reemplazan con 0

# Rellenar columnas específicas
df.fillna({
    "Age": 0,
    "City": "Unknown",
    "Salary": 0.0
}).show()

# Rellenar por tipo de dato
df.fillna({
    "Age": 0,  # Entero
    "City": "Unknown",  # String
    "Salary": 0.0  # Float
}).show()
```

### 8.3 Reemplazar valores específicos

```python
from pyspark.sql.functions import when, col

# Reemplazar valores específicos
df.withColumn(
    "City",
    when(col("City") == "Unknown", "Bangalore").otherwise(col("City"))
).show()

# Reemplazar múltiples valores
from pyspark.sql.functions import create_map, lit
from itertools import chain

mapping = create_map(
    list(chain(*[
        (lit(x), lit(y)) for x, y in 
        [("Unknown", "Bangalore"), ("N/A", "Pune"), ("Error", "New Delhi")]
    ]))
)

df.withColumn("City", mapping[col("City")]).show()
```

## 9. Operaciones con Columnas

### 9.1 Crear nuevas columnas

```python
from pyspark.sql.functions import col, lit, concat

# Agregar columna con valor constante
df.withColumn("Country", lit("India")).show()

# Agregar columna basada en otra
df.withColumn("Age_plus_10", col("Age") + 10).show()

# Concatenar columnas
df.withColumn(
    "Full_Info",
    concat(col("Name"), lit(" - "), col("City"))
).show()
```

### 9.2 Modificar columnas existentes

```python
# Modificar columna existente
df.withColumn("Age", col("Age") + 1).show()

# Modificar con condición
from pyspark.sql.functions import when

df.withColumn(
    "Age_Group",
    when(col("Age") < 30, "Young")
    .when(col("Age").between(30, 40), "Middle")
    .otherwise("Senior")
).show()
```

### 9.3 Renombrar columnas

```python
# Renombrar una columna
df.withColumnRenamed("City", "Location").show()

# Renombrar múltiples columnas
df.select(
    col("Name").alias("EmployeeName"),
    col("City").alias("Location"),
    col("Age").alias("EmployeeAge")
).show()
```

## 10. Operaciones de Conjuntos

### 10.1 Union (UNION ALL)

```python
# Unir dos DataFrames (mantiene duplicados)
df1.union(df2).show()

# Union con el mismo esquema
df_2023 = df.filter(col("Year") == 2023)
df_2024 = df.filter(col("Year") == 2024)
df_all = df_2023.union(df_2024)
```

### 10.2 Union DISTINCT

```python
# Unir y eliminar duplicados
df1.union(df2).distinct().show()
```

### 10.3 Intersectar

```python
# Solo registros que están en AMBOS DataFrames
df1.intersect(df2).show()
```

### 10.4 Except (Diferencia)

```python
# Registros en df1 pero NO en df2
df1.exceptAll(df2).show()  # Mantiene duplicados
df1.subtract(df2).show()  # Elimina duplicados
```

## 11. Operaciones con Strings

### 11.1 Funciones de texto comunes

```python
from pyspark.sql.functions import col, lower, upper, trim, length, substring

# Convertir a minúsculas/mayúsculas
df.select(
    col("City"),
    lower(col("City")).alias("city_lower"),
    upper(col("City")).alias("city_upper")
).show()

# Eliminar espacios
df.select(
    trim(col("City")).alias("city_trimmed")
).show()

# Longitud del texto
df.select(
    col("City"),
    length(col("City")).alias("city_length")
).show()

# Substring
df.select(
    col("City"),
    substring(col("City"), 1, 3).alias("city_prefix")
).show()
```

## 12. Operaciones con Fechas

### 12.1 Funciones de fecha comunes

```python
from pyspark.sql.functions import col, year, month, dayofmonth, current_date

# Extraer partes de una fecha
df.select(
    col("JoiningDate"),
    year(col("JoiningDate")).alias("year"),
    month(col("JoiningDate")).alias("month"),
    dayofmonth(col("JoiningDate")).alias("day")
).show()

# Fecha actual
df.select(current_date().alias("today")).show()
```

## 13. Ejemplo Práctico Completo

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, avg, sum, isnan

# Crear sesión de Spark
spark = SparkSession.builder.appName("BasicOperations").getOrCreate()

# Leer datos
df = spark.read.csv("Employee.csv", header=True, inferSchema=True)

# 1. Contar registros
print(f"Total registros: {df.count()}")

# 2. Detectar nulos
print("\n=== Registros con City nulo ===")
df.filter(col("City").isNull()).show()

# 3. Contar nulos por columna
print("\n=== Conteo de nulos por columna ===")
for column in df.columns:
    null_count = df.filter(col(column).isNull()).count()
    print(f"{column}: {null_count} nulos")

# 4. Filtrar datos
print("\n=== Empleados de Bangalore mayores de 30 ===")
df.filter(
    (col("City") == "Bangalore") & (col("Age") > 30)
).show()

# 5. Agregaciones
print("\n=== Estadísticas por Ciudad ===")
df.groupBy("City").agg(
    count("*").alias("total_employees"),
    avg("Age").alias("avg_age"),
    avg("Salary").alias("avg_salary")
).show()

# 6. Rellenar nulos
print("\n=== Después de rellenar nulos ===")
df_clean = df.fillna({
    "City": "Unknown",
    "Age": 0,
    "Salary": 0.0
})
df_clean.show()

# 7. Eliminar duplicados
print("\n=== Después de eliminar duplicados ===")
df_unique = df.dropDuplicates(["EmployeeID"])
print(f"Registros únicos: {df_unique.count()}")
```

## 14. Mejores Prácticas

### 14.1 Rendimiento

```python
# ✅ BUENO: Filtrar antes de contar
df.filter(col("City") == "Bangalore").count()

# ❌ MALO: Contar todo y luego filtrar
df.filter(col("City") == "Bangalore").count()  # Menos eficiente
```

### 14.2 Evitar operaciones costosas

```python
# ✅ BUENO: Usar select() para limitar columnas
df.select("Name", "City", "Age").filter(col("Age") > 30).show()

# ❌ MALO: Procesar todas las columnas
df.filter(col("Age") > 30).show()
```

### 14.3 Usar funciones de PySpark

```python
# ✅ BUENO: Usar funciones nativas de PySpark
from pyspark.sql.functions import upper
df.select(upper(col("City")))

# ❌ MALO: Usar funciones de Python (UDF)
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf

def upper_py(s):
    return s.upper()

upper_udf = udf(upper_py, StringType())
df.select(upper_udf(col("City")))
```

## Resumen de Funciones Más Utilizadas

| Operación | Función PySpark |
|-----------|----------------|
| Filtrar nulos | `col("x").isNull()` |
| Filtrar NaN | `isnan(col("x"))` |
| Contar | `df.count()` |
| Contar por grupo | `df.groupBy("x").count()` |
| Filtrar | `df.filter(condición)` |
| Seleccionar | `df.select("col1", "col2")` |
| Ordenar | `df.orderBy("col")` |
| Eliminar duplicados | `df.dropDuplicates(["col"])` |
| Rellenar nulos | `df.fillna(valor)` |
| Eliminar nulos | `df.dropna()` |
| Agregar columna | `df.withColumn("new", expr)` |
| Renombrar | `df.withColumnRenamed("old", "new")` |

## Recursos Adicionales

- [Documentación oficial de PySpark DataFrame](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html)
- [Funciones de PySpark](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [Operaciones comunes en DataFrames](https://spark.apache.org/docs/latest/sql-ref-syntax.html)