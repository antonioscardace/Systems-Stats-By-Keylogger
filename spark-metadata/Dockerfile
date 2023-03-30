FROM jupyter/pyspark-notebook:spark-3.1.1

LABEL mantainer="Antonio Scardace" 

RUN pip3 install --no-cache-dir pyspark numpy elasticsearch deep_translator requests

WORKDIR /usr/app/spark-metadata/
COPY ./src/ .
COPY ./titles/ ./titles/

ENTRYPOINT ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1", "--master", "local[5]", "cluster.py"]