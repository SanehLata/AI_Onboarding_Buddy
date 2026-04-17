# API Gateway

## Overview
TechCorp uses Kong API Gateway as the single entry point for all client-facing API traffic. It handles authentication verification, rate limiting, request routing, and observability.

## Architecture
- **Deployment**: Kong 3.4 running on EKS with 3 replicas (auto-scaling to 10).
- **Database**: PostgreSQL for Kong configuration storage.
- **Admin API**: `kong-admin.techcorp.internal:8001` (VPN required).
- **Proxy**: `api.techcorp.com:443` (public) and `api.techcorp.internal:8000` (internal).

## Routing
| Route Pattern | Upstream Service | Auth Required |
|---------------|-----------------|---------------|
| `/api/v1/auth/*` | Authentication Service | No (login endpoints) |
| `/api/v1/payments/*` | Payment Service | Yes (Bearer token) |
| `/api/v1/users/*` | User Service | Yes (Bearer token) |
| `/api/v1/notifications/*` | Notification Service | Yes (Bearer token) |
| `/api/v1/health` | Health aggregator | No |

## Key Plugins
- **JWT Auth**: Validates Bearer tokens on protected routes using the Auth Service's public key.
- **Rate Limiting**: 100 requests/minute per API key (configurable per route).
- **CORS**: Configured for approved frontend domains.
- **Request Transformer**: Adds `X-Request-ID` header for distributed tracing.
- **Datadog**: Exports metrics and traces to Datadog for monitoring.

## Adding a New Route
1. Define the upstream service in Kong's declarative config (`kong.yaml`).
2. Add the route with path matching and required plugins.
3. Test in dev environment first: `dev.techcorp.internal`.
4. Deploy via CI/CD pipeline (Kong config is version-controlled in GitHub).

## Troubleshooting
- **502 Bad Gateway**: Upstream service is down or unreachable. Check pod health in Kubernetes.
- **429 Too Many Requests**: Rate limit exceeded. Check if the client is sending burst traffic.
- **401 Unauthorized**: Token expired or invalid. Verify with `/api/v1/auth/userinfo`.

## Monitoring
Kong metrics are available in the Datadog dashboard: `Kong Gateway Overview`. Key metrics to watch: request rate, error rate (5xx), and p99 latency.
