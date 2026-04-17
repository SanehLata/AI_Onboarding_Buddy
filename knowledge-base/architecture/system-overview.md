# System Overview

## Architecture Summary
TechCorp's platform is a distributed microservices architecture running on AWS EKS (Kubernetes). Services communicate via REST APIs and async messaging through Amazon SQS/SNS. Data is stored across PostgreSQL (transactional), Snowflake (analytics), and Redis (caching).

## Core Services
- **API Gateway** (Kong): Entry point for all client requests. Handles authentication, rate limiting, and routing.
- **Authentication Service**: Manages user identity, OAuth 2.0 tokens, and session management. Integrates with Azure AD for SSO.
- **Payment Service**: Processes payment transactions, manages payment methods, and handles settlement with banking partners.
- **Data Pipeline**: Ingests events from all services, transforms data, and loads into Snowflake for analytics and reporting.
- **Notification Service**: Sends emails, SMS, and push notifications triggered by business events.

## Infrastructure
- **Cloud**: AWS (primary), with Azure AD for identity management.
- **Container Orchestration**: Amazon EKS (Kubernetes 1.28).
- **CI/CD**: Jenkins pipelines with GitHub Actions for PR checks.
- **Monitoring**: Datadog for metrics and alerts, ELK Stack for logs, PagerDuty for incident management.
- **Infrastructure as Code**: Terraform for all cloud resources.

## Environments
| Environment | Purpose | URL |
|-------------|---------|-----|
| Local | Developer workstations | localhost |
| Dev | Integration testing | dev.techcorp.internal |
| Staging | Pre-production validation | staging.techcorp.internal |
| Production | Live traffic | api.techcorp.com |

## Key Design Decisions
- Event-driven architecture for loose coupling between services.
- Database-per-service pattern — each service owns its data.
- Blue-green deployments for zero-downtime releases.
- Circuit breaker pattern for resilient inter-service communication.
