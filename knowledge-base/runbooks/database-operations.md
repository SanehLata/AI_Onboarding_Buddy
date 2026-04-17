# Database Operations

## Database Landscape
| Database | Engine | Purpose | Access |
|----------|--------|---------|--------|
| Auth DB | PostgreSQL 15 | User credentials, sessions, tokens | auth-dev AD group |
| Payments DB | PostgreSQL 15 | Transactions, payment methods, refunds | payments-dev AD group |
| Analytics | Snowflake | Reporting, dashboards, ML features | DATA_READER role |
| Cache | Redis 7 | Session cache, rate limiting, feature flags | Via application only |

## Connecting to Databases

### PostgreSQL (Dev/Staging)
```bash
# Via VPN — connection details in your team's .env file
psql -h <hostname> -U <username> -d <database>

# Or use a GUI client (DBeaver, pgAdmin, DataGrip)
```

### Snowflake
```bash
# Install snowsql CLI
brew install snowflake-snowsql  # macOS

# Connect
snowsql -a techcorp.us-east-1 -u your.name@techcorp.com -d TECHCORP_ANALYTICS -w ENGINEERING_WH
```

## Schema Migrations
All schema changes go through a migration pipeline:
1. Write migration using Alembic (Python) in the service's `migrations/` directory.
2. Test migration in local Docker environment.
3. Run migration in staging via Jenkins pipeline.
4. Production migration runs as part of the deployment pipeline (pre-deploy step).

```bash
# Create a new migration
alembic revision --autogenerate -m "add_column_to_transactions"

# Apply locally
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

## Backup and Recovery
- PostgreSQL: Automated daily snapshots via AWS RDS. 30-day retention. Point-in-time recovery available within 5 minutes.
- Snowflake: Time Travel enabled (90 days). Query historical data with `AT(TIMESTAMP => '2025-01-01 00:00:00')`.
- Redis: No backups (cache is ephemeral by design). Services must handle cache misses gracefully.

## Query Performance Guidelines
- Always use indexes for WHERE clauses on large tables (>1M rows).
- Avoid `SELECT *` — specify only needed columns.
- Use `EXPLAIN ANALYZE` to check query plans before deploying new queries.
- Long-running queries (>30s) are automatically killed in production.

## Emergency Database Access
For production database access during incidents, contact the DBA on-call via `dba-oncall@techcorp.com` or the #database Slack channel. Direct production access requires VP Engineering approval and is logged to the audit trail.
