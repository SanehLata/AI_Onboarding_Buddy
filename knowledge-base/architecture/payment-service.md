# Payment Service

## Overview
The Payment Service processes financial transactions, manages payment methods, and handles settlement with banking partners. It is the most business-critical service in the platform with strict uptime requirements (99.99% SLA).

## Technology Stack
- Runtime: Python 3.11 + FastAPI
- Database: PostgreSQL 15 (primary-replica with automatic failover)
- Message Queue: Amazon SQS for async transaction processing
- External Integrations: Stripe (card processing), Plaid (bank verification)

## Core Workflows

### Payment Processing
1. Client submits payment request via API Gateway.
2. Payment Service validates the request (amount, currency, payment method).
3. Fraud check runs synchronously via the risk scoring engine.
4. If approved, transaction is submitted to Stripe for processing.
5. Result (success/failure) is persisted to PostgreSQL.
6. Event published to SNS topic `payment.completed` for downstream consumers.

### Refund Processing
1. Refund request validated against original transaction.
2. Partial or full refund submitted to Stripe.
3. Refund event published for accounting reconciliation.

## API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/payments` | POST | Create a new payment |
| `/payments/{id}` | GET | Retrieve payment details |
| `/payments/{id}/refund` | POST | Initiate a refund |
| `/payments/methods` | GET | List saved payment methods |
| `/payments/methods` | POST | Add a new payment method |

## Data Model
- `transactions` table: id, amount, currency, status, payment_method_id, created_at
- `payment_methods` table: id, user_id, type, provider_token, is_default
- `refunds` table: id, transaction_id, amount, status, reason

## Error Handling
All payment operations are idempotent. Clients must include an `Idempotency-Key` header to prevent duplicate transactions. The service uses the outbox pattern to guarantee exactly-once event publishing.

## Security
- PCI DSS Level 1 compliant. No raw card numbers stored — all tokenised via Stripe.
- All payment endpoints require `payments:write` OAuth scope.
- Sensitive fields encrypted at rest using AWS KMS.

## On-Call Notes
Payment failures trigger PagerDuty alerts at P1 severity. See the Incident Response runbook for escalation procedures. Common issues: Stripe API rate limits (check Datadog dashboard `payments-health`), database connection pool exhaustion (restart pods via kubectl).
