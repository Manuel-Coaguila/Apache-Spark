"""
Módulo central de configuración.
Lee config.yaml (datos no sensibles) + obtiene credenciales de os.getenv().
Las variables de entorno se inyectan desde docker-compose (env_file: .env.prod).

NOTA: El logging se inicializa en main.py, no aquí.
Si este módulo se importa antes de que main.py configure el logging,
los mensajes se pierden. Por eso se usa print() como fallback.
"""
import os
import yaml
import logging

logger = logging.getLogger("etl.spark_config")

try:
    # Leer config.yaml (datos no sensibles)
    _config_path = '/opt/spark/projects/proyecto_001/conf/config.yaml'
    with open(_config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Agregar credenciales desde variables de entorno (inyectadas por docker-compose)
    config["sqlserver"]["username"] = os.getenv("SQLSERVER_USER_P001")
    config["sqlserver"]["password"] = os.getenv("SQLSERVER_PASSWORD_P001")

#    logger.info("Variables cargadas correctamente")

except Exception as e:
    # Fallback a print porque el logging puede no estar configurado aún
    print(f"[config.py] ERROR: {e}")
    logger.error("Error en config.py: %s", e, exc_info=True)
    raise