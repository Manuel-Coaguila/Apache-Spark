from pyspark.sql import functions as F
import os
from dotenv import load_dotenv

dotenv_path = '/opt/spark/spark-projects/Proyecto_001/conf/.env.Proyecto_001'
load_dotenv(dotenv_path=dotenv_path)

user = os.environ["SQLSERVER_USER_P001"]
password = os.environ["SQLSERVER_PASSWORD_P001"]
database = os.environ["SQLSERVER_DATABASE_P001"]
hostname = os.environ["SQLSERVER_HOSTNAME_PP01"]
port = os.environ["SQLSERVER_PORT_P001"]
driver = os.environ["SQLSERVER_DRIVER_P001"]


def run(df):
    # Ruta de salida para CSV
    output_csv = "/opt/spark/spark-projects/Proyecto_001/files/output/Employee_with_date_csv"
    #os.makedirs(output_csv, exist_ok=True)
    df.write.csv(output_csv, header=True, mode="overwrite")
    print(f"Archivo CSV guardado en: {output_csv}")

    # Ruta de salida para Parquet
    output_parquet = "/opt/spark/spark-projects/Proyecto_001/files/output/Employee_with_date_parquet"
    #os.makedirs(output_parquet, exist_ok=True)
    df.write.parquet(output_parquet, mode="overwrite")
    print(f"Archivo Parquet guardado en: {output_parquet}")

        # 🔹 Guardar en SQL Server
    jdbc_url = f"jdbc:sqlserver://{hostname}:{port};databaseName={database};encrypt=false;trustServerCertificate=true"
    connection_properties = {
        "user": f"{user}",
        "password": f"{password}",
        "driver": f"{driver}"}

    (
       df.write.
       mode("overwrite").
       option("batchsize",1000).
       jdbc(url=jdbc_url, table="Employee_with_date", properties=connection_properties)
    )

    print("DataFrame cargado en tabla SQL Server: Employee_with_date")