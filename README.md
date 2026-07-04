# Proyecto Apache Spark - Guía de Diseño y Nomenclatura

## 1. Propósito

Este documento define las reglas de diseño, estructura y nomenclatura para el proyecto `apache_spark`. Está pensado para un ambiente productivo, por lo que las convenciones deben ser estrictas, consistentes y fáciles de mantener.

## 2. Estructura de carpetas recomendada

La estructura base del proyecto debe ser clara y separada por responsabilidades:

- `apache_spark/`
  - `.env`                  : Variables de entorno de configuración.
  - `Dockerfile`            : Imagen Docker del entorno Spark.
  - `docker-compose.yaml`   : Orquestación de servicios.
  - `requirements.txt`      : Dependencias Python.
  - `extra-jars/`           : JARs externos necesarios para Spark.
  - `Projects/`             : Proyectos o pipelines individuales.
  - `shared/`               : Código compartido entre proyectos.
  - `README.md`             : Documentación del proyecto.

Dentro de cada proyecto:

- `Projects/Proyecto_001/`
  - `config/`             : Configuración de base de datos, Spark, logging.
  - `etl/`                : Módulos de extracción, transformación, carga y validación.
  - `files/`              : Archivos de entrada/salida de datos.
  - `logs/`               : Registros de ejecución.
  - `schemas/`            : Definición de esquemas de datos.
  - `tests/`              : Pruebas unitarias y de integración.
  - `main.py`             : Punto de entrada del pipeline.

## 3. Convenciones generales de nomenclatura

### 3.1 Variables de entorno

- Usar `UPPER_SNAKE_CASE`.
- Usar prefijo de ámbito o servicio para agrupar variables.
- Usar sufijos claros para el tipo de valor.
- No usar espacios, acentos o caracteres especiales.
- Mantener nombres estables y predecibles.

Ejemplos:

- `SQLSERVER_USER`
- `SQLSERVER_PASSWORD`
- `SQLSERVER_DATABASE`
- `SQLSERVER_HOST`
- `SQLSERVER_PORT`
- `SQLSERVER_DRIVER`
- `SQLSERVER_JDBC_JAR`
- `SPARK_MASTER_HOST_GENERALES`
- `SPARK_WORKER_MEMORY_GENERALES`
- `NAME_PROJECT_P001`

### 3.2 Prefijos y ámbitos

Usar prefijos para separar dominios de configuración:

- `SQLSERVER_` para variables de conexión SQL Server.
- `SPARK_` para variables del cluster Spark.
- `PROJECT_` para variables específicas de un proyecto.
- `GENERAL_` o `GENERALES_` para configuración global compartida.

### 3.3 Archivos y módulos Python

- Archivos: `lower_snake_case.py`.
- Módulos/directorios: `lower_snake_case/`.
- Clases: `PascalCase`.
- Funciones: `snake_case`.
- Constantes de módulo: `UPPER_SNAKE_CASE`.

Ejemplos:

- `spark_config.py`
- `extract.py`
- `transform.py`
- `load.py`
- `validation.py`
- `database.yaml`
- `logging.yaml`

### 3.4 Variables Python

- Variables locales y argumentos: `snake_case`.
- Nombres descriptivos y cortos.
- Evitar abreviaturas ambiguas.
- Usar verbos para funciones y sustantivos para datos.

Ejemplos:

- `spark_session`
- `jdbc_url`
- `connection_properties`
- `output_path`
- `dataframe_clean`

## 4. Reglas específicas para variables de entorno

1. `UPPER_SNAKE_CASE` obligatorio.
2. Prefijo de servicio o proyecto obligatorio.
3. El valor debe ser un valor literal, no lógica.
4. Las variables sensibles deben manejarse como secretos en producción y no versionarse en repositorios públicos.
5. Los nombres deben ser autoexplicativos y fáciles de leer.

### Ejemplos del `.env`

```env
SQLSERVER_USER=sa
SQLSERVER_PASSWORD=Manuel1999!
SQLSERVER_DATABASE=DWH
SQLSERVER_PORT=1433
SQLSERVER_DRIVER=com.microsoft.sqlserver.jdbc.SQLServerDriver
SQLSERVER_JDBC_JAR=/opt/spark/extra-jars/mssql-jdbc-13.4.0.jre11.jar

JDBC_JAR_PATH_GENERALES=/opt/spark/extra-jars/mssql-jdbc-12.6.3.jre8.jar
SPARK_MASTER_HOST_GENERALES=spark-master
SPARK_MASTER_CORES_GENERALES=2
SPARK_MASTER_MEMORY_GENERALES=2g
SPARK_WORKER_CORES_GENERALES=2
SPARK_WORKER_MEMORY_GENERALES=2g

NAME_PROJECT_P001=PROYECTO_001
SPARK_EXECUTOR_MEMORY_P001=2g
SPARK_EXECUTOR_CORES_P001=2
SPARK_DRIVER_MEMORY_P001=2g
SPARK_DRIVER_CORES_P001=2
```

## 5. Buenas prácticas de diseño

- Separar lógica de configuración y código.
- Mantener el pipeline modular: extracción, transformación y carga deben ser independientes.
- No hardcodear credenciales ni rutas en el código.
- Usar variables de entorno para valores productivos.
- Documentar cada variable y cada archivo de configuración.
- Usar pruebas en `tests/` para asegurar transformaciones y cargas.

## 6. Uso recomendado en producción

- Cargar variables de entorno desde `.env` solo en desarrollo.
- En producción, usar el gestor de secretos de la plataforma.
- No escribir valores sensibles en `README.md` ni en repositorios.
- Mantener `requirements.txt` actualizado y versionado.
- Validar que `Dockerfile` y `docker-compose.yaml` utilizan las rutas correctas.

## 7. Resumen de nomenclatura para el proyecto

- Carpetas: `lower_snake_case`
- Archivos Python: `lower_snake_case.py`
- Clases: `PascalCase`
- Funciones y variables Python: `snake_case`
- Variables de entorno: `UPPER_SNAKE_CASE`
- Prefijos: `SQLSERVER_`, `SPARK_`, `PROJECT_`, `GENERAL_`

Con estas reglas, el proyecto mantendrá un estándar profesional y consistente acorde a un ambiente productivo.