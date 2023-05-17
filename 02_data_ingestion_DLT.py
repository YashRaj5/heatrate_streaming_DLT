# Databricks notebook source
# MAGIC %md
# MAGIC ### Architecture
# MAGIC ![KafkaStream](https://raw.githubusercontent.com/fmunz/kafka-dlt-streaminganalytics/main/images/kafka.jpg)

# COMMAND ----------

# DBTITLE 1,Importing Libraries
import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

TOPIC = "heartbeat_sim_data"
# KAFKA_BROKER = spark.conf.get("KAFKA_SERVER")
KAFKA_BROKER = "pkc-56d1g.eastus.azure.confluent.cloud:9092"
# confluentApiKey = spark.conf.get("confluentApiKey")
confluentApiKey="Z5NHE2DJIUBYDJ5T"
# confluentSecret = spark.conf.get("confluentSecret")
confluentSecret = "7YSfjIjuMJSzbD1LTi+E66pGQmyCJM/j9rfeLOIy4OuzF4gSX+sEqIAzCv/GjT+7"

# subscribe to TOPIC at KAFKA_BROKER
# ConfluentCloud is using Simple Authentication and Security Layer (SASL)

raw_kafka_events = (spark.readStream
    .format("kafka")
    .option("subscribe", TOPIC)
    .option("kafka.bootstrap.servers", KAFKA_BROKER)
    .option("kafka.security.protocol", "SASL_SSL")
    .option("kafka.sasl.jaas.config", "kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username='{}' password='{}';".format(confluentApiKey, confluentSecret))
    .option("kafka.ssl.endpoint.identification.algorithm", "https")
    .option("kafka.sasl.mechanism", "PLAIN")
    .option("failOnDataLoss", "false")
    .option("startingOffsets", "earliest")
    .load()
    )

# no special keyword for streaming tables in Python DLT, just return stream

# table_properties={"pipelines.reset.allowed":"false"} prevents table refresh

reset = "true"

@dlt.table(comment="The data ingested from kafka topic",
           table_properties={"pipelines.reset.allowed": reset}
          )
def kafka_events():
  return raw_kafka_events

# COMMAND ----------

# MAGIC %md
# MAGIC The spark Kafka data source does not allow schema inference, we have to define it

# COMMAND ----------

# define the schema 
# example event: {'ip': '54.65.54.189', 'time': '2022-04-11 12:46:37.476076', 'version': 6, 'model': 'fitbit', 'color': 'navy', 'heart_bpm': 69, 'kcal': 2534} 
event_schema = StructType([ \
    StructField("ip", StringType(),True), \
    StructField("time", TimestampType(),True)      , \
    StructField("version", StringType(),True), \
    StructField("model", StringType(),True)     , \
    StructField("color", StringType(),True)     , \
    StructField("heart_bpm", IntegerType(),True), \
    StructField("kcal", IntegerType(),True)       \
  ])

# COMMAND ----------

# DBTITLE 1,Decoding JSON format using Schema defined above in DLT
# temporary table = alias, visible in pipeline but not in data browser, cannot be queried interactively
@dlt.table(comment="real schema for Kakfa payload",
           table_properties={"pipelines.reset.allowed": reset},
           temporary=True)

def bpm_raw():
  return (
    # kafka streams are (timestamp,value) with value containing the kafka payload, i.e. event
    # no automatic schema inference!
    dlt.read_stream("kafka_events")
    .select(col("timestamp"), 
     from_json(col("value").cast("string"), event_schema).alias("event"))
    .select("timestamp", "event.*")     
  )


# COMMAND ----------

# DBTITLE 1,Cleansing the table
@dlt.table()
@dlt.expect_or_drop("heart rate is set", "bpm IS NOT NULL")
@dlt.expect_or_drop("event time is set", "time IS NOT NULL")
@dlt.expect_or_drop("human has pulse >0", "bpm > 0")
@dlt.expect_or_drop("tracker is valid", "model <> 'undef' ")

def bpm_cleansed(table_properties={"pipelines.reset.allowed": reset}):
  return (
    dlt.read_stream("bpm_raw")
    .withColumnRenamed("heart_bpm", "bpm")
    .select("time", "bpm", "model") 
    
  )

# COMMAND ----------

# DBTITLE 1,Streaming Analytics with DLT
# Global Aggregations (not based on time)
@dlt.table(name="global_stat")
def bpm_global():
  return (
    dlt.read_stream("bpm_cleansed").groupBy()
    .agg(count('bpm').alias('eventsTotal'),
         max('bpm').alias('max'),
         min('bpm').alias('min'),
         avg('bpm').alias('average'),
         stddev('bpm').alias('stddev')
        )
  )
