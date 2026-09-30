# Predictive Maintenance Analytics Using Databricks

## Project Overview

This project implements a data engineering and predictive maintenance analytics solution using **Databricks Medallion Architecture**.

The objective is to transform raw industrial machine data into clean, analytical datasets that can help maintenance teams understand machine health, error patterns, failures, maintenance effectiveness, and reliability.

The project uses machine information, sensor telemetry, machine errors, maintenance events, and failure records.

---

## Business Problem

Industrial machines generate large volumes of sensor and maintenance data. Unexpected failures can lead to:

* Production downtime
* Increased maintenance costs
* Equipment damage
* Production delays
* Reduced operational efficiency

This project analyzes historical machine data to identify failure patterns, abnormal sensor behavior, maintenance trends, and machine reliability indicators.

---

## Dataset

The project uses the following datasets:

| Dataset       | Description                                        |
| ------------- | -------------------------------------------------- |
| `machines`    | Machine ID, model and machine age                  |
| `telemetry`   | Voltage, rotation, pressure and vibration readings |
| `errors`      | Machine error events and error types               |
| `maintenance` | Maintenance events and affected components         |
| `failures`    | Machine failure events and failed components       |

---

## Technology Stack

* Databricks
* Databricks SQL
* SQL
* Delta Tables
* Medallion Architecture
* Bronze / Silver / Gold layers
* Statistical analysis
* Predictive maintenance analytics

---

# Medallion Architecture

```text
                    RAW CSV DATA
                         |
                         v
                +----------------+
                |  BRONZE LAYER  |
                |                |
                | Raw machine    |
                | telemetry      |
                | errors         |
                | maintenance    |
                | failures       |
                +----------------+
                         |
                         v
                +----------------+
                |  SILVER LAYER  |
                |                |
                | Cleaning       |
                | Null handling  |
                | Deduplication  |
                | Standardization|
                +----------------+
                         |
                         v
                +----------------+
                |   GOLD LAYER   |
                |                |
                | Machine Health |
                | Error Summary  |
                | Maintenance    |
                | Failure History|
                | Predictive     |
                | Features       |
                +----------------+
                         |
                         v
              BUSINESS ANALYSIS
                         |
                         v
              PREDICTIVE MAINTENANCE
```

---

# Bronze Layer

The Bronze layer stores the raw source data with minimal transformation.

### Bronze tables

* `tseries.bronze_machines`
* `tseries.bronze_telemetry`
* `tseries.bronze_errors`
* `tseries.bronze_maint`
* `tseries.bronze_failures`

---

# Silver Layer

The Silver layer prepares the data for analysis.

The following data quality operations were performed:

* Removed invalid records
* Handled NULL values
* Removed blank values
* Trimmed text fields
* Standardized component and failure names
* Removed duplicate records
* Removed unnecessary `_rescued_data` columns
* Applied basic validation rules

### Silver tables

* `tseries.silver_machines`
* `tseries.silver_telemetry`
* `tseries.silver_errors`
* `tseries.silver_maint`
* `tseries.silver_failures`

---

# Gold Layer

The Gold layer contains business-ready analytical datasets.

### Gold tables

#### 1. Machine Health

`tseries.gold_machine_health`

Combines machine information with telemetry measurements.

#### 2. Error Summary

`tseries.gold_error_summary`

Contains:

* Total errors
* Unique error types
* First error time
* Last error time

#### 3. Maintenance Summary

`tseries.gold_maintenance_summary`

Contains:

* Total maintenance events
* Components maintained
* First maintenance time
* Last maintenance time

#### 4. Failure History

`tseries.gold_failure_history`

Contains:

* Total failures
* Failure types
* First failure time
* Last failure time

#### 5. Predictive Features

`tseries.gold_predictive_features`

Contains machine-level features such as:

* Average voltage
* Maximum/minimum voltage
* Average rotation
* Maximum/minimum rotation
* Average pressure
* Maximum/minimum pressure
* Average vibration
* Maximum/minimum vibration
* Total errors
* Maintenance events
* Failure counts
* Failure flag

---

# Business Questions Solved

## 1. Error vs Failure Analysis

**Question:**
Do machine errors occur before component failures?

**Analysis:**
Error events were analyzed within 24–48 hours before failures.

**Purpose:**
Identify error patterns that may serve as early warning indicators.

---

## 2. Machine Age and Model Analysis

**Question:**
How do machine age and model affect baseline sensor behavior?

**Analysis:**
Telemetry metrics were compared across machine age groups and models.

**Metrics:**

* Voltage
* Rotation
* Pressure
* Vibration

---

## 3. Maintenance and Sensor Stability

**Question:**
Does sensor behavior change as time passes after maintenance?

**Analysis:**
Telemetry behavior was compared based on the number of days since the previous maintenance event.

---

## 4. Telemetry Forecasting

**Question:**
Can future telemetry behavior be estimated from recent sensor readings?

**Analysis:**
Recent telemetry averages were used as a baseline forecast for future sensor values.

**Future enhancement:**
Implement time-series models such as LSTM, ARIMA or Prophet.

---

## 5. Multi-Sensor Anomaly Detection

**Question:**
Can abnormal machine conditions be detected without relying on error codes?

**Analysis:**
Statistical anomaly scores were calculated using multiple telemetry sensors.

Sensors analyzed:

* Voltage
* Rotation
* Pressure
* Vibration

---

## 6. 24-Hour Failure Risk Analysis

**Question:**
How frequently does a machine experience a failure within 24 hours after a telemetry observation?

**Analysis:**
Historical telemetry observations were compared with failures occurring within the next 24 hours.

**Future enhancement:**
Build a machine-learning classification model to generate an actual failure probability.

---

## 7. Component Failure Analysis

**Question:**
Which components fail most frequently?

**Analysis:**
Failure events were grouped by component and related error events were analyzed.

**Purpose:**
Identify frequently failing components and common preceding errors.

---

## 8. Maintenance-to-Failure / RUL Analysis

**Question:**
How long does a machine operate after maintenance before the next failure?

**Analysis:**
The time between maintenance events and subsequent failures was calculated.

Metrics:

* Average time to failure
* Minimum time to failure
* Maximum time to failure

**Future enhancement:**
Develop a true Remaining Useful Life (RUL) regression model.

---

## 9. Preventive Maintenance Effectiveness

**Question:**
How frequently are failures observed after maintenance events?

**Analysis:**
Maintenance events were compared with subsequent failure events.

Metrics:

* Maintenance events
* Maintenance events followed by failure
* Failure-after-maintenance percentage
* Average time to failure

---

## 10. Machine Reliability / MTBF

**Question:**
How does reliability differ across machine models?

**Analysis:**
Time between consecutive failures was calculated to estimate Mean Time Between Failures (MTBF).

Metrics:

* Average MTBF
* Minimum MTBF
* Maximum MTBF
* Failure count

---

# Key Analytical Areas

The project therefore covers five major predictive-maintenance areas:

| Area                      | Questions  |
| ------------------------- | ---------- |
| Error Analysis            | Q1         |
| Machine & Sensor Analysis | Q2, Q4, Q5 |
| Maintenance Analysis      | Q3, Q8, Q9 |
| Failure Analysis          | Q1, Q6, Q7 |
| Reliability Analysis      | Q10        |

---

# Predictive Maintenance Workflow

```text
Machine Data
     +
Telemetry
     +
Errors
     +
Maintenance
     +
Failures
     |
     v
Bronze
     |
     v
Data Cleaning
     |
     v
Silver
     |
     v
Feature Engineering
     |
     v
Gold
     |
     +--------------------+
     |                    |
     v                    v
Statistical         Predictive ML
Analysis            Models
     |                    |
     v                    v
Anomaly Detection   Failure Prediction
     |              RUL Prediction
     v              Forecasting
Maintenance Insights
```

---

# Future Enhancements

The current project establishes the data engineering and SQL analytics foundation.

Future ML enhancements can include:

1. **Failure prediction model**

   * Random Forest
   * XGBoost
   * Logistic Regression

2. **Remaining Useful Life prediction**

   * Regression models
   * Time-series models

3. **Telemetry forecasting**

   * LSTM
   * ARIMA
   * Prophet

4. **Advanced anomaly detection**

   * Isolation Forest
   * Autoencoders

5. **AI Maintenance Agent**

   * Natural-language interaction with the Gold tables
   * Machine health summaries
   * Failure-risk explanations
   * Maintenance recommendations based on available historical data

---

# Project Outcome

The project transforms raw industrial machine data into structured, analysis-ready datasets using Databricks Medallion Architecture.

It provides analytical capabilities for:

* Machine health monitoring
* Error pattern analysis
* Failure analysis
* Maintenance analysis
* Anomaly detection
* Reliability analysis
* Failure-risk analysis
* Maintenance-to-failure analysis
* Predictive maintenance feature generation

The architecture also provides a foundation for integrating machine-learning models and an AI-powered predictive maintenance agent in future development.
