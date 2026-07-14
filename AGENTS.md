# AGENTS.md - Apache Spark ETL Project

## Stack
- **Apache Spark 4.0.3** (Scala 2.13, Java 17, Python 3) on Ubuntu
- Dockerized: `spark-master` + `spark-worker` via `docker-compose.yaml`
- Python deps: only `PyYAML==6.0.2` (in `requirements.txt`)
- JDBC driver: `extra_jars/mssql-jdbc-12.6.3.jre8.jar` (copied to `/opt/spark/jars/` in Dockerfile)

## Repo Structure
```
apache_spark/
├── Dockerfile              # FROM apache/spark:4.0.3-scala2.13-java17-python3-ubuntu
├── docker-compose.yaml     # master (:7077, :8081) + worker, net tesis-net (external)
├── requirements.txt        # PyYAML==6.0.2
├── .env                    # Credenciales + config (gitignored)
├── conf/
│   ├── logging.yaml        # EMPTY (root level, unused)
│   ├── spark-defaults.conf # Spark tuning + auth config
│   └── env/
│       ├── .env.dev        # EMPTY
│       └── .env.staging    # EMPTY
├── extra_jars/             # JARs copiados a /opt/spark/jars/ en build
├── projects/
│   └── proyecto_001/       # Único proyecto ETL actual
│       ├── main.py         # Entrypoint del pipeline
│       ├── src/
│       │   ├── etl/        # extract.py → transform.py → validation.py → load.py
│       │   ├── functions/  # Capas de limpieza: clean, flag, normalize_*
│       │   ├── schemas/    # Tipos: StructType con todos StringType
│       │   ├── config/  # config.py (lee config.yaml + env vars)
│       │   └── sesion/  # get_spark_session()
│       ├── conf/           # config.yaml + logging.yaml (proyecto-level)
│       ├── files/input/    # CSV fuente (Employee.csv)
│       ├── files/output/   # CSV + Parquet generados (gitignored)
│       ├── logs/           # etl.log (gitignored)
│       ├── tests/          # TODO: empty stubs (__init__, test_extract, test_transform, test_load)
│       └── docs/           # basic_operations.md, joins_examples.md
└── logs/                   # Event logs de Spark (gitignored)
```

## Commands
```bash
# Build and start
docker compose --env-file .env build --no-cache
docker compose --env-file .env up -d

# Run ETL (inside container)
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark/projects/proyecto_001/main.py

# Or interactive session
docker exec -it spark-master pyspark --master spark://spark-master:7077
```

## Critical Quirks

### 1. Import order matters
`src/config/config.py` loads YAML at **module level**. It must be imported **after** logging is configured. The entrypoint in `main.py` initializes logging before any `from src.etl import extract` (which transitively imports `config.py`). Adding new modules that import `config.py` at module level must follow this pattern.

### 2. All paths are Docker paths
- Config path: `/opt/spark/projects/proyecto_001/conf/config.yaml`
- Log config: `/opt/spark/projects/proyecto_001/conf/logging.yaml`
- Input file: `/opt/spark/projects/proyecto_001/files/input/Employee.csv`
- Output: `/opt/spark/projects/proyecto_001/files/output/`
Never use relative or host paths in Python code.

### 3. Secrets via env vars
Non-sensitive config in `conf/config.yaml`, credentials injected via `docker-compose.yaml` → `.env` → `os.getenv()` in `config.py`. The `.env` file is gitignored. Agent must not hardcode secrets.

### 4. No test runner configured
`tests/` dir contains empty stubs. No `pytest.ini`, `pyproject.toml`, or `setup.cfg`. If adding tests, need to choose a runner (pytest expected) and add to `requirements.txt`.

### 5. Root `conf/logging.yaml` is empty
The working logging config is at **project level**: `projects/proyecto_001/conf/logging.yaml`. The root-level one exists but has no content.

### 6. Schema: all StringType
All columns are read as `StringType` — no numeric enums, no dates. Cleaning converts strings ("ERROR" sentinel for invalid values). Integer columns stay as strings with possible "ERROR" values.

### 7. SQL Server loading is commented out
`load.py` writes CSV + Parquet only. The JDBC write to SQL Server is blocked out. Uncommenting requires JDBC driver to be present at `/opt/spark/jars/mssql-jdbc-12.6.3.jre8.jar`.

### 8. No Makefile
No build shortcuts. All operations are manual `docker compose` + `docker exec`.

### 9. CI/CD is stubbed
`.github/workflows/ci.yaml` and `deploy.yaml` are empty files.

### 10. Docker build context
Dockerfile uses `--chown=${SPARK_USER}:${SPARK_GROUP}` for all COPY instructions. The user inside container is `uspark` (UID/GID 1000:1000, configurable via build args).

## Architecture — 3 containers
This project is part of a 3-container architecture simulating a production environment:

| Container | Hostname | Description |
|-----------|----------|-------------|
| **SQL Server** | `sql_server_2019` | Database (separate project, its own compose) |
| **Spark** | `spark-master` / `spark-worker` | ETL engine (this project) |
| **Airflow** | `airflow` | Orchestrator (separate project, its own compose) |

All connected via external network `tesis-net`.

## Startup Order
Containers must start in this order due to dependencies:

1. **SQL Server** — `docker compose up -d` (in its own project)
2. **Apache Spark** — `docker compose --env-file .env up -d`
3. **Apache Airflow** — `docker compose up -d` (in its own project)

## Network
- External Docker network `tesis-net` must exist: `docker network create tesis-net`
- Spark master at `spark://spark-master:7077`
- Spark worker connects via `spark://spark-master:7077`
- SQL Server at `sql_server_2019:1433`
- Airflow connects to Spark via `spark-submit` pointing to `spark://spark-master:7077`
