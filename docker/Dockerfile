# Imagen base de Spark
FROM apache/spark:4.0.3-scala2.13-java17-python3-ubuntu

# Variables de build
ARG UID=1000
ARG GID=1000
ARG SPARK_USER=uspark
ARG SPARK_GROUP=gspark
ENV SPARK_HOME=/opt/spark

USER root
RUN addgroup --gid ${GID} ${SPARK_GROUP} && \
    useradd -m -u ${UID} -g ${SPARK_GROUP} ${SPARK_USER} && \
    mkdir -p ${SPARK_HOME}/shared \
             ${SPARK_HOME}/extra-jars \
             ${SPARK_HOME}/spark-projects \
             ${SPARK_HOME}/data \
             ${SPARK_HOME}/conf \
             ${SPARK_HOME}/output \
             ${SPARK_HOME}/work \
             ${SPARK_HOME}/logs/events \
             ${SPARK_HOME}/logs/history && \
    chown -R ${SPARK_USER}:${SPARK_GROUP} \
                ${SPARK_HOME}/shared \
                ${SPARK_HOME}/extra-jars \
                ${SPARK_HOME}/spark-projects \
                ${SPARK_HOME}/data \
                ${SPARK_HOME}/conf \
                ${SPARK_HOME}/output \
                ${SPARK_HOME}/work \
                ${SPARK_HOME}/logs/events \
                ${SPARK_HOME}/logs/history


# Copiar configuraciones de Spark
COPY --chown=${SPARK_USER}:${SPARK_GROUP} ./conf/logging.yaml ${SPARK_HOME}/conf/logging.yaml
COPY --chown=${SPARK_USER}:${SPARK_GROUP} ./conf/spark-defaults.conf ${SPARK_HOME}/conf/spark-defaults.conf
COPY --chown=${SPARK_USER}:${SPARK_GROUP} ./docker/requirements.txt ${SPARK_HOME}/requirements.txt

# Definir directorio de configuración de Spark
ENV SPARK_CONF_DIR=${SPARK_HOME}/conf

# Instalar dependencias Python
RUN pip install --no-cache-dir -r ${SPARK_HOME}/requirements.txt

USER ${SPARK_USER}
WORKDIR ${SPARK_HOME}
