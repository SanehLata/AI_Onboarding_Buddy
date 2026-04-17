# Data Pipeline

## Overview
The data pipeline ingests events from all microservices, transforms them, and loads into Snowflake for analytics, reporting, and ML model training. It processes approximately 50 million events per day.

## Architecture
- **Ingestion**: Amazon Kinesis Data Streams captures events from all services in real time.
- **Processing**: Apache Spark on Amazon EMR performs transformations, deduplication, and enrichment.
- **Storage**: Raw events land in S3 (data lake), transformed data loads into Snowflake.
- **Orchestration**: Apache Airflow manages DAG scheduling and dependency resolution.
- **Schema Registry**: Confluent Schema Registry enforces Avro schemas for all event types.

## Key Data Flows
1. **Transactional events** → Kinesis → Spark → Snowflake `analytics.transactions`
2. **User activity events** → Kinesis → Spark → Snowflake `analytics.user_activity`
3. **System metrics** → Datadog → S3 archive (90-day retention)
4. **ML feature store** → Spark → S3 parquet files → SageMaker training jobs

## Snowflake Access
- Database: `TECHCORP_ANALYTICS`
- Warehouse: `ENGINEERING_WH` (medium, auto-suspend 5 min)
- Roles: `DATA_READER` (read-only), `DATA_ENGINEER` (read-write)
- Connection: Use the Snowflake VS Code extension or `snowsql` CLI

## Airflow DAGs
| DAG | Schedule | Purpose |
|-----|----------|---------|
| `daily_transaction_etl` | 02:00 UTC | Process previous day's transactions |
| `hourly_user_activity` | Every hour | Aggregate user activity metrics |
| `weekly_reporting` | Sunday 06:00 UTC | Generate weekly business reports |
| `ml_feature_refresh` | Daily 04:00 UTC | Update ML feature store |

## Data Quality
- Great Expectations runs validation checks on every pipeline output.
- Data freshness alerts fire if a DAG is delayed by more than 2 hours.
- Schema evolution is handled via backward-compatible Avro changes only.

## Access for New Developers
Request Snowflake access through the Access Provisioning Guide. You'll receive `DATA_READER` role by default. `DATA_ENGINEER` requires manager approval. Airflow UI is available at `airflow.techcorp.internal` (VPN required).
