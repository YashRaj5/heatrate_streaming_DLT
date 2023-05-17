# Databricks notebook source
# MAGIC %md
# MAGIC When we have a fever our resting heart-rate goes up, and our heart rates can be easily measured by or smart watches that we wear on our wrists. With this data source we can help identify the health of a person and probably figure out some trend in their heart rythm, which could be caused by some diesase.
# MAGIC
# MAGIC One such application is to detect if a person has COVID or not by looking at their heart-rate.

# COMMAND ----------

# DBTITLE 1,Installing Required Libraries
# !/databricks/python3/bin/python -m pip install --upgrade pip
!/local_disk0/.ephemeral_nfs/envs/pythonEnv-e8d69d2d-e5f6-4ad8-8868-6a197bceea6c/bin/python -m pip install --upgrade pip
!pip install faker colorama
!pip install confluent-kafka

# COMMAND ----------

# MAGIC %run ./00_kafka_config

# COMMAND ----------

# DBTITLE 1,Importing Required libraries
from faker import Faker
from datetime import datetime
from confluent_kafka import Producer

from colorama import Fore
from colorama import Style

import json
import random, time
import numpy as np

# COMMAND ----------

_ = spark.sql("CREATE DATABASE IF NOT EXISTS heart_stream;")
# - = spark.sql("USE heart_stream;")

# COMMAND ----------

# DBTITLE 1,Setting Up Producer
conf = {'bootstrap.servers': bootstrapServers,
        'security.protocol': "SASL_SSL",
        'sasl.username': confluentApiKey, 
        'sasl.password': confluentApiSecret,
        'ssl.endpoint.identification.algorithm': "https",
        'sasl.mechanism': "PLAIN"
         }

# creating Producer instance
p = Producer(**conf)

# init Faker()
f = Faker()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Defining the Simulated Data

# COMMAND ----------

# returns elapsed minutes/n as in since start
def pulse_inc():
  global time_start
  minutes_diff = int((datetime.now() - time_start).total_seconds() / 60.0 / 3 )
  return minutes_diff



# create fitness tracker event 
def create_event():
  # IP address
  ip = f.ipv4_public()
  
  #event time
  time = str(datetime.now())
  
  # one of many trackers or undef
  [tracker] = random.choices(
              population=["Apple Watch", "Garmin", "Fitbit", "undef"],
              weights=[0.4, 0.3, 0.2, 0.1])
  
  # tracker color 
  color = f.safe_color_name()
  # tracker version 
  version = random.randrange(3, 7)
  
  # bpm is normal distribution + bias (minutes)
  pulse = int(np.random.normal(90, 10)) + pulse_inc()
  [bpm] = random.choices(
          population=[pulse, 0],
          weights=[0.95, 0.05])
  
  kcal = int(np.random.normal(2800, 400))
  
  #return event
  event = {"ip": ip, "time":time, "version":version, "model": tracker, "color": color, "heart_bpm":bpm, "kcal":kcal}
  return event

# COMMAND ----------

# DBTITLE 1,Error Handeling
def delivery_callback(err, msg):
        if err:
            sys.stderr.write('Message failed delivery: {err}')
        else:
            print(f'{Fore.GREEN}(p:{msg.partition()} o:{msg.offset()}) {Style.RESET_ALL}',end=' - ')

# COMMAND ----------

# publishing event to TOPIC @ BROKER
def publish_event (event):
  global counter
  try:
    # Produce line (without newline)
    p.produce(topic, json.dumps(event).encode('utf-8'), callback=delivery_callback)

  except BufferError:
      print(f'%% Local producer queue is full {len(p)} messages awaiting delivery: try again\n')

    # Serve delivery callback queue.
    # NOTE: Since produce() is an asynchronous API this poll() call
    #       will most likely not serve the delivery callback for the
    #       last produce()d message.
  counter +=1
  print(f'{Fore.BLUE}{counter}{Style.RESET_ALL}',end=" - ")

# COMMAND ----------

counter = 0                    # init counter 
time_start = datetime.now()    # baseline time

# send events until interrupted
# number of events and pause between events varies

while (True):
  # send x to y events in a burst
  for _ in range(random.randrange(12, 27)):
    event = (create_event())
    publish_event(event)
    
  p.poll(0)  
  #wait between x an y seconds
  time.sleep(random.randrange(2, 6))

# COMMAND ----------

dbutils.notebook.exit("here be dragons")

# COMMAND ----------

topic

# COMMAND ----------

# check events
event = create_event()
print (event)

# COMMAND ----------

# check manually
publish_event(event)

# COMMAND ----------

minutes_elapsed()
