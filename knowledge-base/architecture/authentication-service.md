# Authentication Service

## Overview
The Authentication Service manages user identity and access control for all TechCorp applications. It implements OAuth 2.0 and OpenID Connect, integrating with Azure Active Directory for enterprise SSO.

## Technology Stack
- Runtime: Python 3.11 + FastAPI
- Database: PostgreSQL 15 (dedicated instance)
- Cache: Redis 7 for session and token caching
- Identity Provider: Azure AD via MSAL library

## Authentication Flow
1. Client sends credentials to `/auth/token` endpoint.
2. Service validates against Azure AD (for SSO) or local credentials.
3. On success, issues a JWT access token (15-min expiry) and refresh token (7-day expiry).
4. Access tokens are validated by the API Gateway on every request.
5. Refresh tokens can be exchanged for new access tokens at `/auth/refresh`.

## API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/auth/token` | POST | Issue access + refresh tokens |
| `/auth/refresh` | POST | Exchange refresh token for new access token |
| `/auth/revoke` | POST | Revoke a refresh token (logout) |
| `/auth/userinfo` | GET | Return current user profile |
| `/auth/.well-known/openid-configuration` | GET | OIDC discovery document |

## Security Controls
- All tokens are signed with RS256 (asymmetric keys rotated quarterly).
- Rate limiting: 10 login attempts per minute per IP.
- Account lockout after 5 failed attempts (30-minute cooldown).
- All authentication events are logged to the audit trail.

## Local Development
The auth service runs locally via Docker Compose. Use the mock Azure AD provider for local testing — credentials are in the team `.env.example` file.
