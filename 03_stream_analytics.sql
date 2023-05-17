-- Databricks notebook source
-- MAGIC %md
-- MAGIC ### Global Statistics

-- COMMAND ----------

select *  from heart_stream.global_stat

-- COMMAND ----------

select count(*)  from heart_stream.bpm_cleansed

-- COMMAND ----------

select model, count (*) as c  from heart_stream.bpm_cleansed group by model order by c

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql.functions import *

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Streaming Data Analytics 
-- MAGIC streaming data: BPM aggregated over x minute [tumbling window](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC display(spark.readStream.format("delta").table("heart_stream.bpm_cleansed").
-- MAGIC         groupBy("bpm",window("time", "1 minute")).avg("bpm").orderBy("window",ascending=True))
