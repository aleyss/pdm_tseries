# Databricks notebook source
# MAGIC %sql
# MAGIC SHOW SCHEMAS IN tseries;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES IN tseries.tseries;

# COMMAND ----------

# MAGIC %sql
# MAGIC LIST '/Volumes/tseries/tseries/tseries/';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.bronze_machines
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM read_files(
# MAGIC     '/Volumes/tseries/tseries/tseries/PdM_machines.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.bronze_telemetry
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM read_files(
# MAGIC     '/Volumes/tseries/tseries/tseries/PdM_telemetry.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.bronze_errors
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM read_files(
# MAGIC     '/Volumes/tseries/tseries/tseries/PdM_errors.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.bronze_maint
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM read_files(
# MAGIC     '/Volumes/tseries/tseries/tseries/PdM_maint.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.bronze_failures
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM read_files(
# MAGIC     '/Volumes/tseries/tseries/tseries/PdM_failures.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN tseries.tseries;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tseries.tseries.bronze_machines LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tseries.tseries.bronze_telemetry LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tseries.tseries.bronze_errors LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tseries.tseries.bronze_maint LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tseries.tseries.bronze_failures LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'machines' AS table_name, COUNT(*) AS row_count
# MAGIC FROM tseries.tseries.bronze_machines
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'telemetry', COUNT(*)
# MAGIC FROM tseries.tseries.bronze_telemetry
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'errors', COUNT(*)
# MAGIC FROM tseries.tseries.bronze_errors
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'maintenance', COUNT(*)
# MAGIC FROM tseries.tseries.bronze_maint
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'failures', COUNT(*)
# MAGIC FROM tseries.tseries.bronze_failures;

# COMMAND ----------

