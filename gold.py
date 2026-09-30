# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.gold_machine_health AS
# MAGIC SELECT
# MAGIC     m.machineID,
# MAGIC     m.model,
# MAGIC     m.age,
# MAGIC     t.datetime,
# MAGIC     t.volt,
# MAGIC     t.rotate,
# MAGIC     t.pressure,
# MAGIC     t.vibration
# MAGIC FROM tseries.tseries.silver_machines m
# MAGIC INNER JOIN tseries.tseries.silver_telemetry t
# MAGIC     ON m.machineID = t.machineID;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     m.machineID,
# MAGIC     m.model,
# MAGIC     m.age,
# MAGIC     t.datetime,
# MAGIC     t.volt,
# MAGIC     t.rotate,
# MAGIC     t.pressure,
# MAGIC     t.vibration
# MAGIC FROM tseries.tseries.silver_machines m
# MAGIC INNER JOIN tseries.tseries.silver_telemetry t
# MAGIC     ON m.machineID = t.machineID;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM tseries.tseries.gold_machine_health
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.gold_error_summary AS
# MAGIC SELECT
# MAGIC     machineID,
# MAGIC     COUNT(*) AS total_errors,
# MAGIC     COUNT(DISTINCT errorID) AS unique_error_types,
# MAGIC     MIN(datetime) AS first_error_time,
# MAGIC     MAX(datetime) AS last_error_time
# MAGIC FROM tseries.tseries.silver_errors
# MAGIC GROUP BY machineID;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM tseries.tseries.gold_error_summary
# MAGIC ORDER BY total_errors DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.gold_maintenance_summary AS
# MAGIC SELECT
# MAGIC     machineID,
# MAGIC     COUNT(*) AS total_maintenance_events,
# MAGIC     COUNT(DISTINCT comp) AS components_maintained,
# MAGIC     MIN(datetime) AS first_maintenance_time,
# MAGIC     MAX(datetime) AS last_maintenance_time
# MAGIC FROM tseries.tseries.silver_maint
# MAGIC GROUP BY machineID;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM tseries.tseries.gold_maintenance_summary
# MAGIC ORDER BY total_maintenance_events DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.gold_failure_history AS
# MAGIC SELECT
# MAGIC     machineID,
# MAGIC     COUNT(*) AS total_failures,
# MAGIC     COUNT(DISTINCT failure) AS failure_types,
# MAGIC     MIN(datetime) AS first_failure_time,
# MAGIC     MAX(datetime) AS last_failure_time
# MAGIC FROM tseries.tseries.silver_failures
# MAGIC GROUP BY machineID;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM tseries.tseries.gold_failure_history
# MAGIC ORDER BY total_failures DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC predictive maintenance features

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE tseries.tseries.gold_predictive_features AS
# MAGIC
# MAGIC SELECT
# MAGIC     m.machineID,
# MAGIC     m.model,
# MAGIC     m.age,
# MAGIC
# MAGIC     /* Telemetry */
# MAGIC     COUNT(t.datetime) AS telemetry_records,
# MAGIC
# MAGIC     AVG(t.volt) AS avg_voltage,
# MAGIC     MAX(t.volt) AS max_voltage,
# MAGIC     MIN(t.volt) AS min_voltage,
# MAGIC
# MAGIC     AVG(t.rotate) AS avg_rotation,
# MAGIC     MAX(t.rotate) AS max_rotation,
# MAGIC     MIN(t.rotate) AS min_rotation,
# MAGIC
# MAGIC     AVG(t.pressure) AS avg_pressure,
# MAGIC     MAX(t.pressure) AS max_pressure,
# MAGIC     MIN(t.pressure) AS min_pressure,
# MAGIC
# MAGIC     AVG(t.vibration) AS avg_vibration,
# MAGIC     MAX(t.vibration) AS max_vibration,
# MAGIC     MIN(t.vibration) AS min_vibration,
# MAGIC
# MAGIC     /* Errors */
# MAGIC     COALESCE(e.total_errors, 0) AS total_errors,
# MAGIC     COALESCE(e.unique_error_types, 0) AS unique_error_types,
# MAGIC
# MAGIC     /* Maintenance */
# MAGIC     COALESCE(mt.total_maintenance_events, 0)
# MAGIC         AS total_maintenance_events,
# MAGIC
# MAGIC     COALESCE(mt.components_maintained, 0)
# MAGIC         AS components_maintained,
# MAGIC
# MAGIC     /* Failures */
# MAGIC     COALESCE(f.total_failures, 0)
# MAGIC         AS total_failures,
# MAGIC
# MAGIC     COALESCE(f.failure_types, 0)
# MAGIC         AS failure_types,
# MAGIC
# MAGIC     /* Target */
# MAGIC     CASE
# MAGIC         WHEN COALESCE(f.total_failures, 0) > 0
# MAGIC         THEN 1
# MAGIC         ELSE 0
# MAGIC     END AS failure_flag
# MAGIC
# MAGIC FROM tseries.tseries.silver_machines m
# MAGIC
# MAGIC LEFT JOIN tseries.tseries.silver_telemetry t
# MAGIC     ON m.machineID = t.machineID
# MAGIC
# MAGIC LEFT JOIN tseries.tseries.gold_error_summary e
# MAGIC     ON m.machineID = e.machineID
# MAGIC
# MAGIC LEFT JOIN tseries.tseries.gold_maintenance_summary mt
# MAGIC     ON m.machineID = mt.machineID
# MAGIC
# MAGIC LEFT JOIN tseries.tseries.gold_failure_history f
# MAGIC     ON m.machineID = f.machineID
# MAGIC
# MAGIC GROUP BY
# MAGIC     m.machineID,
# MAGIC     m.model,
# MAGIC     m.age,
# MAGIC     e.total_errors,
# MAGIC     e.unique_error_types,
# MAGIC     mt.total_maintenance_events,
# MAGIC     mt.components_maintained,
# MAGIC     f.total_failures,
# MAGIC     f.failure_types;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM tseries.tseries.gold_predictive_features
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     failure_flag,
# MAGIC     COUNT(*) AS machine_count
# MAGIC FROM tseries.tseries.gold_predictive_features
# MAGIC GROUP BY failure_flag;

# COMMAND ----------

# MAGIC %sql
# MAGIC show tables in tseries.tseries;

# COMMAND ----------

