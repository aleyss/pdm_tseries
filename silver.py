# Databricks notebook source
# MAGIC %sql
# MAGIC DESCRIBE tseries.tseries.bronze_machines;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE tseries.tseries.bronze_telemetry;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE tseries.tseries.bronze_errors;
# MAGIC     
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE tseries.tseries.bronze_maint;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE tseries.tseries.bronze_failures;

# COMMAND ----------

# MAGIC %md
# MAGIC 1.data cleaning
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.silver_machines AS
# MAGIC SELECT
# MAGIC     machineID,
# MAGIC     TRIM(model) AS model,
# MAGIC     age
# MAGIC FROM tseries.tseries.bronze_machines
# MAGIC WHERE machineID IS NOT NULL
# MAGIC   AND model IS NOT NULL
# MAGIC   AND TRIM(model) <> ''
# MAGIC   AND age IS NOT NULL
# MAGIC   AND age >= 0
# MAGIC QUALIFY ROW_NUMBER() OVER (
# MAGIC     PARTITION BY machineID
# MAGIC     ORDER BY machineID
# MAGIC ) = 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.silver_telemetry AS
# MAGIC SELECT
# MAGIC     datetime,
# MAGIC     machineID,
# MAGIC     volt,
# MAGIC     rotate,
# MAGIC     pressure,
# MAGIC     vibration
# MAGIC FROM tseries.tseries.bronze_telemetry
# MAGIC WHERE datetime IS NOT NULL
# MAGIC   AND machineID IS NOT NULL
# MAGIC   AND volt IS NOT NULL
# MAGIC   AND rotate IS NOT NULL
# MAGIC   AND pressure IS NOT NULL
# MAGIC   AND vibration IS NOT NULL
# MAGIC   AND volt >= 0
# MAGIC   AND rotate >= 0
# MAGIC   AND pressure >= 0
# MAGIC   AND vibration >= 0
# MAGIC QUALIFY ROW_NUMBER() OVER (
# MAGIC     PARTITION BY datetime, machineID
# MAGIC     ORDER BY datetime
# MAGIC ) = 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.silver_errors AS
# MAGIC SELECT
# MAGIC     datetime,
# MAGIC     machineID,
# MAGIC     TRIM(errorID) AS errorID
# MAGIC FROM tseries.tseries.bronze_errors
# MAGIC WHERE datetime IS NOT NULL
# MAGIC   AND machineID IS NOT NULL
# MAGIC   AND errorID IS NOT NULL
# MAGIC   AND TRIM(errorID) <> ''
# MAGIC QUALIFY ROW_NUMBER() OVER (
# MAGIC     PARTITION BY datetime, machineID, errorID
# MAGIC     ORDER BY datetime
# MAGIC ) = 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.silver_maint AS
# MAGIC SELECT
# MAGIC     datetime,
# MAGIC     machineID,
# MAGIC     UPPER(TRIM(comp)) AS comp
# MAGIC FROM tseries.tseries.bronze_maint
# MAGIC WHERE datetime IS NOT NULL
# MAGIC   AND machineID IS NOT NULL
# MAGIC   AND comp IS NOT NULL
# MAGIC   AND TRIM(comp) <> ''
# MAGIC QUALIFY ROW_NUMBER() OVER (
# MAGIC     PARTITION BY datetime, machineID, comp
# MAGIC     ORDER BY datetime
# MAGIC ) = 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.silver_failures AS
# MAGIC SELECT
# MAGIC     datetime,
# MAGIC     machineID,
# MAGIC     UPPER(TRIM(failure)) AS failure
# MAGIC FROM tseries.tseries.bronze_failures
# MAGIC WHERE datetime IS NOT NULL
# MAGIC   AND machineID IS NOT NULL
# MAGIC   AND failure IS NOT NULL
# MAGIC   AND TRIM(failure) <> ''
# MAGIC QUALIFY ROW_NUMBER() OVER (
# MAGIC     PARTITION BY datetime, machineID, failure
# MAGIC     ORDER BY datetime
# MAGIC ) = 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC show tables in tseries.tseries;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM tseries.tseries.silver_machines
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC checking nulls

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(machineID) AS machine_ids,
# MAGIC     COUNT(model) AS models,
# MAGIC     COUNT(age) AS ages
# MAGIC FROM tseries.tseries.silver_machines;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(datetime) AS timestamps,
# MAGIC     COUNT(machineID) AS machine_ids,
# MAGIC     COUNT(volt) AS volt_values,
# MAGIC     COUNT(rotate) AS rotate_values,
# MAGIC     COUNT(pressure) AS pressure_values,
# MAGIC     COUNT(vibration) AS vibration_values
# MAGIC FROM tseries.tseries.silver_telemetry;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(datetime) AS timestamps,
# MAGIC     COUNT(machineID) AS machine_ids,
# MAGIC     COUNT(errorID) AS error_ids
# MAGIC FROM tseries.tseries.silver_errors;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(datetime) AS timestamps,
# MAGIC     COUNT(machineID) AS machine_ids,
# MAGIC     COUNT(comp) AS components
# MAGIC FROM tseries.tseries.silver_maint;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_rows,
# MAGIC     COUNT(datetime) AS timestamps,
# MAGIC     COUNT(machineID) AS machine_ids,
# MAGIC     COUNT(failure) AS failures
# MAGIC FROM tseries.tseries.silver_failures;

# COMMAND ----------

