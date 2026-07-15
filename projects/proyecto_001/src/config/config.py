
import os
import yaml
import logging

logger = logging.getLogger("etl.config")

try:
    # logger.info("Configurando las ENV y config")
    # Leer config.yaml (datos no sensibles)
    _config_path = '/opt/spark/projects/proyecto_001/conf/config.yaml'
    with open(_config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Agregar credenciales desde variables de entorno (inyectadas por docker-compose)
    config["sqlserver"]["username"] = os.getenv("SQLSERVER_USER_P001")
    config["sqlserver"]["password"] = os.getenv("SQLSERVER_PASSWORD_P001")
    config["paths"]["logging"] = os.getenv("PATH_LOGGING_P001")

#    logger.info("Variables cargadas correctamente")

except Exception as e:
    # Fallback a print porque el logging puede no estar configurado aún
    logger.error("Error en config.py: %s", e, exc_info=True)
    raise
