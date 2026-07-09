"""
Módulo central de configuración.
Lee config.yaml (datos no sensibles) + obtiene credenciales de os.getenv().
Las variables de entorno se inyectan desde docker-compose (env_file: .env.prod).
"""
import os
import yaml

# Leer config.yaml (datos no sensibles)
_config_path = '/opt/spark/projects/proyecto_001/conf/config.yaml'
with open(_config_path, 'r') as f:
    config = yaml.safe_load(f)

# Agregar credenciales desde variables de entorno (inyectadas por docker-compose)
config["sqlserver"]["username"] = os.getenv("SQLSERVER_USER_P001")
config["sqlserver"]["password"] = os.getenv("SQLSERVER_PASSWORD_P001")