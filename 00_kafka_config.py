# Databricks notebook source
# DBTITLE 1,Kafka Configurations for Databricks Connector
# MAGIC %md
# MAGIC bootstrap.servers=pkc-56d1g.eastus.azure.confluent.cloud:9092
# MAGIC key.converter=org.apache.kafka.connect.storage.StringConverter
# MAGIC value.converter=org.apache.kafka.connect.json.JsonConverter
# MAGIC value.converter.schemas.enable=false
# MAGIC
# MAGIC ssl.endpoint.identification.algorithm=https
# MAGIC security.protocol=SASL_SSL
# MAGIC sasl.mechanism=PLAIN
# MAGIC sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="R6J5YOIC5RTK36DE" password="Kav/qB1UmTnGko2pDtu2l3rSkL9y6Zqe9Bjnb/9MD03iJpkn9YMhUloMQcBnE/r+";
# MAGIC request.timeout.ms=20000
# MAGIC retry.backoff.ms=500
# MAGIC
# MAGIC producer.bootstrap.servers=pkc-56d1g.eastus.azure.confluent.cloud:9092
# MAGIC producer.ssl.endpoint.identification.algorithm=https
# MAGIC producer.security.protocol=SASL_SSL
# MAGIC producer.sasl.mechanism=PLAIN
# MAGIC producer.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="R6J5YOIC5RTK36DE" password="Kav/qB1UmTnGko2pDtu2l3rSkL9y6Zqe9Bjnb/9MD03iJpkn9YMhUloMQcBnE/r+";
# MAGIC producer.request.timeout.ms=20000
# MAGIC producer.retry.backoff.ms=500
# MAGIC
# MAGIC consumer.bootstrap.servers=pkc-56d1g.eastus.azure.confluent.cloud:9092
# MAGIC consumer.ssl.endpoint.identification.algorithm=https
# MAGIC consumer.security.protocol=SASL_SSL
# MAGIC consumer.sasl.mechanism=PLAIN
# MAGIC consumer.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="R6J5YOIC5RTK36DE" password="Kav/qB1UmTnGko2pDtu2l3rSkL9y6Zqe9Bjnb/9MD03iJpkn9YMhUloMQcBnE/r+";
# MAGIC consumer.request.timeout.ms=20000
# MAGIC consumer.retry.backoff.ms=500
# MAGIC
# MAGIC offset.flush.interval.ms=10000
# MAGIC offset.storage.file.filename=/tmp/connect.offsets

# COMMAND ----------

topic = "heartbeat_sim_data"
bootstrapServers="pkc-56d1g.eastus.azure.confluent.cloud:9092"

# confluent cloud keys
confluentApiKey="Z5NHE2DJIUBYDJ5T"
confluentApiSecret="7YSfjIjuMJSzbD1LTi+E66pGQmyCJM/j9rfeLOIy4OuzF4gSX+sEqIAzCv/GjT+7"
