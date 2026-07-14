
# Imagen base de Spark
FROM apache/spark:4.0.3-scala2.13-java17-python3-ubuntu

# Instalar Python 3.13
USER root
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3.13 python3.13-venv python3.13-dev && \
    ln -sf /usr/bin/python3.13 /usr/bin/python3 && \
    python3 -m ensurepip --upgrade && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    rm -rf /var/lib/apt/lists/*

ENV PYSPARK_PYTHON=/usr/bin/python3.13
ENV PYSPARK_DRIVER_PYTHON=/usr/bin/python3.13

ARG UID=1000
ARG GID=1000
ARG SPARK_USER=uspark
ARG SPARK_GROUP=gspark
ENV SPARK_HOME=/opt/spark

RUN addgroup --gid ${GID} ${SPARK_GROUP} && \
    useradd -m -u ${UID} -g ${SPARK_GROUP} ${SPARK_USER} && \
    mkdir -p ${SPARK_HOME}/projects \
             ${SPARK_HOME}/extra_jars \
             ${SPARK_HOME}/conf \
             ${SPARK_HOME}/output \
             ${SPARK_HOME}/work \
             ${SPARK_HOME}/logs/events \
             ${SPARK_HOME}/logs/history && \
    chown -R ${SPARK_USER}:${SPARK_GROUP} \
             ${SPARK_HOME}/projects \
             ${SPARK_HOME}/conf \
             ${SPARK_HOME}/output \
             ${SPARK_HOME}/work \
             ${SPARK_HOME}/logs/events \
             ${SPARK_HOME}/logs/history

#COPY --chown=${SPARK_USER}:${SPARK_GROUP} ./conf/logging.yaml ${SPARK_HOME}/conf/logging.yaml
COPY --chown=${SPARK_USER}:${SPARK_GROUP} ./conf/spark-defaults.conf ${SPARK_HOME}/conf/spark-defaults.conf
COPY --chown=${SPARK_USER}:${SPARK_GROUP} ./requirements.txt ${SPARK_HOME}/requirements.txt
COPY --chown=${SPARK_USER}:${SPARK_GROUP} ./extra_jars/ ${SPARK_HOME}/jars/

#ENV SPARK_CONF_DIR=${SPARK_HOME}/conf

RUN pip install --no-cache-dir -r ${SPARK_HOME}/requirements.txt

USER ${SPARK_USER}
WORKDIR ${SPARK_HOME}
