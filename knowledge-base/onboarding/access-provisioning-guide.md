# Access Provisioning Guide

## Overview
System access is provisioned automatically by the AI Onboarding Buddy based on your team and role. This guide explains what access you receive and how to verify it.

## Access Types

### Jira/ServiceNow Tickets
A ServiceNow ticket (TKT-XXXXX) is raised for each system requiring manual provisioning. Track ticket status at `servicenow.techcorp.com`. Typical SLA: 4-8 business hours.

### Distribution List (DL) Subscriptions
Email subscriptions to team and cross-functional distribution lists. Automatically processed within 24 business hours. You'll receive a confirmation email for each DL.

### Active Directory (AD) Group Membership
AD groups control access to repositories, CI/CD pipelines, and cloud environments. Requires manager approval via Teams Approvals before activation.

## Team-Based Access Matrix

| Team | Systems | DL Groups | AD Groups |
|------|---------|-----------|-----------|
| Payments | GitHub, Jenkins, AWS, Stripe Dashboard, Datadog, Confluence | payments-eng, payments-alerts, all-engineering | payments-dev, aws-payments-dev, github-payments |
| Risk & Compliance | GitHub, Jenkins, AWS, Snowflake, Datadog, Confluence | risk-eng, risk-alerts, compliance-updates, all-engineering | risk-dev, aws-risk-dev, snowflake-analysts |
| Platform Engineering | GitHub, Jenkins, AWS, Kubernetes Dashboard, Terraform Cloud, Datadog | platform-eng, infra-alerts, all-engineering | platform-dev, aws-admin, k8s-admin, terraform-operators |
| Data & Analytics | GitHub, Jenkins, AWS, Snowflake, Airflow, Databricks | data-eng, data-alerts, all-engineering | data-dev, aws-data-dev, snowflake-engineers, airflow-dev |

## Verifying Your Access
1. **ServiceNow**: Go to `servicenow.techcorp.com` > My Tickets to see ticket status.
2. **Email DLs**: Check your Outlook inbox for subscription confirmation emails.
3. **AD Groups**: Try accessing each system. If blocked, check the Onboarding Buddy for the approval status.
4. **GitHub**: Visit `github.techcorp.com` and verify you can see your team's repositories.

## Escalation
If access is not provisioned within the SLA, contact your manager or raise it in the daily standup. For urgent access needs, reach out to IT Helpdesk: helpdesk@techcorp.com.
