# Incident Response Runbook

## Severity Levels
| Severity | Definition | Response Time | Examples |
|----------|-----------|---------------|----------|
| P1 - Critical | Complete service outage or data breach | 15 min (business hours), 30 min (after hours) | Payment processing down, authentication failure, data leak |
| P2 - High | Degraded service affecting >10% of users | 30 min (business hours), 1 hour (after hours) | Slow response times, partial feature failure |
| P3 - Medium | Minor issue with workaround available | 4 business hours | UI glitch, non-critical feature broken |
| P4 - Low | Cosmetic or minor inconvenience | Next business day | Typo in UI, minor logging issue |

## Incident Response Steps

### 1. Acknowledge (0-5 minutes)
- Acknowledge the PagerDuty alert within the response time SLA.
- Join the #incidents Slack channel and post: "Investigating [alert name]. I'm the incident commander."
- Create an incident in ServiceNow with initial severity assessment.

### 2. Assess (5-15 minutes)
- Check Datadog dashboards for the affected service.
- Review recent deployments — was anything deployed in the last 2 hours?
- Check Kubernetes pod health: `kubectl get pods -n production | grep -v Running`
- Determine blast radius: which users/services are affected?

### 3. Mitigate (15-60 minutes)
- If caused by a recent deployment: rollback immediately.
  ```bash
  kubectl rollout undo deployment/<service-name> -n production
  ```
- If caused by a dependency (database, external API): enable circuit breaker or failover.
- If caused by traffic spike: scale up pods.
  ```bash
  kubectl scale deployment/<service-name> --replicas=10 -n production
  ```
- Communicate status updates in #incidents every 15 minutes.

### 4. Resolve
- Confirm the issue is fully resolved with metrics returning to baseline.
- Update the ServiceNow ticket with resolution details.
- Post final status in #incidents: "Incident resolved. Root cause: [brief]. Postmortem scheduled."

### 5. Postmortem (within 48 hours)
- Blameless postmortem document created in Confluence.
- Template: `confluence.techcorp.com/templates/postmortem`
- Must include: timeline, root cause, impact, action items with owners and due dates.
- Review in next team retrospective.

## Escalation Contacts
| Role | Primary | Backup |
|------|---------|--------|
| Engineering Manager | Listed in PagerDuty schedule | VP Engineering |
| Database Admin | dba-oncall@techcorp.com | Database team Slack |
| Security | infosec-oncall@techcorp.com | CISO (P1 only) |
| Communications | comms@techcorp.com | VP Marketing (customer-facing P1) |

## Key Dashboards
- Service health: `datadog.techcorp.com/dashboard/<service>-health`
- Infrastructure: `datadog.techcorp.com/dashboard/k8s-overview`
- Business impact: `datadog.techcorp.com/dashboard/business-metrics`
