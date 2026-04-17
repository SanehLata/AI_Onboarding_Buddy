# Deployment Guide

## Overview
All services are deployed to Amazon EKS using blue-green deployment strategy. Deployments are automated via Jenkins pipelines triggered by merges to the `main` branch.

## Deployment Pipeline
1. **PR merged to main** → Jenkins pipeline triggers automatically.
2. **Build**: Docker image built, tagged with commit SHA and `latest`.
3. **Test**: Integration tests run against a disposable environment.
4. **Push**: Image pushed to Amazon ECR (Elastic Container Registry).
5. **Deploy to staging**: Kubernetes manifests applied to staging cluster.
6. **Smoke tests**: Automated health checks run against staging.
7. **Manual approval**: Deploy to production requires approval in Jenkins (from team lead or on-call engineer).
8. **Deploy to production**: Blue-green switch — new version goes live, old version kept as fallback.
9. **Monitor**: 15-minute observation window. Auto-rollback if error rate exceeds 1%.

## Manual Deployment (Emergency)
```bash
# Authenticate to EKS
aws eks update-kubeconfig --name techcorp-prod --region us-east-1

# Deploy a specific image version
kubectl set image deployment/<service-name> \
  <container-name>=<ecr-repo>:<tag> \
  -n production

# Verify rollout
kubectl rollout status deployment/<service-name> -n production

# Rollback if needed
kubectl rollout undo deployment/<service-name> -n production
```

## Pre-Deployment Checklist
- [ ] All PR checks passing (tests, linting, security scan)
- [ ] Database migrations reviewed and tested in staging
- [ ] Feature flags configured for gradual rollout (if applicable)
- [ ] On-call engineer aware of the deployment
- [ ] Rollback plan documented in the deployment ticket

## Deployment Schedule
- Production deployments: Monday through Thursday, 10:00 AM - 3:00 PM EST only.
- No deployments on Fridays or before holidays.
- Emergency hotfixes: Any time with P1 incident justification and VP approval.

## Monitoring Post-Deployment
Watch these Datadog dashboards for 15 minutes after deployment:
- `<service-name>-health`: Error rate, latency p99, request volume
- `kubernetes-pods`: Pod restarts, OOM kills, CPU/memory usage
- `business-metrics`: Transaction success rate, user activity (if applicable)
