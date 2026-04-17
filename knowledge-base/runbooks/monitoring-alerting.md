# Monitoring and Alerting

## Monitoring Stack
- **Metrics**: Datadog (application + infrastructure metrics)
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana) at `kibana.techcorp.internal`
- **Traces**: Datadog APM with distributed tracing across all services
- **Alerting**: Datadog Monitors → PagerDuty → Slack #incidents

## Key Metrics Per Service
Every service must expose these standard metrics:
- `request_rate`: Requests per second by endpoint and status code
- `error_rate`: Percentage of 5xx responses (alert threshold: >1%)
- `latency_p99`: 99th percentile response time (alert threshold: >500ms)
- `cpu_usage`: Container CPU utilisation (alert threshold: >80%)
- `memory_usage`: Container memory utilisation (alert threshold: >85%)

## Standard Dashboards
| Dashboard | URL | Purpose |
|-----------|-----|---------|
| Service Health | `datadog/dashboard/<service>-health` | Per-service request rate, errors, latency |
| Kubernetes Overview | `datadog/dashboard/k8s-overview` | Pod status, node health, resource usage |
| Business Metrics | `datadog/dashboard/business-metrics` | Transaction volume, user activity, revenue |
| Database Health | `datadog/dashboard/rds-overview` | Query performance, connections, replication lag |

## Alert Configuration
Alerts are defined as code in the `monitoring/` directory of each service repository. Example Datadog monitor definition:
```yaml
name: "High Error Rate - Payment Service"
type: metric alert
query: "avg(last_5m):sum:http.requests{service:payment-service,status_code:5xx}.as_rate() / sum:http.requests{service:payment-service}.as_rate() > 0.01"
thresholds:
  critical: 0.01
  warning: 0.005
notify:
  - "@pagerduty-payments-oncall"
  - "@slack-incidents"
```

## Log Aggregation
All services log in structured JSON format. Key fields: `timestamp`, `level`, `service`, `trace_id`, `message`, `context`. Search logs in Kibana using the trace ID from Datadog to correlate metrics with log entries.

## On-Call Responsibilities
- Check the daily health summary email at 9:00 AM.
- Review any alerts that fired overnight in PagerDuty.
- Monitor the #incidents channel during your on-call shift.
- Handoff notes to the next on-call engineer at the end of your rotation.
