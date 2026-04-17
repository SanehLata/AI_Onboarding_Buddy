# 🤝 AI Onboarding Buddy — Microsoft Copilot Studio Edition

> An agentic AI onboarding system built on Microsoft Copilot Studio, Azure AI Foundry, Power Automate, and Microsoft Graph — automating developer profile intake, access provisioning, learning path generation, and RAG-based Q&A via Teams, with Cosmos DB, Dataverse, and Azure Functions powering the backend.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![Copilot Studio](https://img.shields.io/badge/Copilot_Studio-Framework_Copilot-0078D4?style=flat-square)](https://copilotstudio.microsoft.com)
[![Azure Foundry](https://img.shields.io/badge/Azure_AI_Foundry-GPT--4o-00BCF2?style=flat-square)](https://azure.microsoft.com/products/ai-foundry)
[![Power Automate](https://img.shields.io/badge/Power_Automate-Workflows-0066FF?style=flat-square)](https://make.powerautomate.com)
[![Microsoft Graph](https://img.shields.io/badge/Microsoft_Graph-API-FF6F00?style=flat-square)](https://graph.microsoft.com)
[![Cosmos DB](https://img.shields.io/badge/Cosmos_DB-Thread_Storage-00A86B?style=flat-square)](https://azure.microsoft.com/products/cosmos-db)
[![Teams](https://img.shields.io/badge/Microsoft_Teams-Deployed-6264A7?style=flat-square)](https://teams.microsoft.com)

---

## What It Does

Traditional developer onboarding involves manual ticket-raising, chasing DL owners, reading through wikis, and waiting days for access. **AI Onboarding Buddy** automates the entire process end-to-end through a single Microsoft Teams conversation:

| Step | What the Agent Does |
|------|-------------------|
| **Profile intake** | Collects developer details via natural conversation using generative orchestration |
| **Access provisioning** | Raises tickets, sends DL subscription emails, submits AD group requests via Power Automate + Microsoft Graph |
| **Welcome email** | Sends a real Outlook email to the developer via Microsoft Graph |
| **Calendar invite** | Creates an onboarding kickoff meeting with the developer's manager |
| **Learning path** | Generates a personalised, sequenced reading plan using Azure AI Foundry (GPT-4o) |
| **RAG Q&A** | Answers questions about systems, tools, and processes grounded in SharePoint-hosted knowledge base |
| **Progress tracking** | Tracks which documents the developer has completed |
| **Manager approvals** | Routes access requests to the manager via Teams Approvals |
| **Observability** | Three-layer monitoring: Copilot Studio Analytics, Application Insights, Foundry Control Plane |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Microsoft Teams                             │
│                   (User Interface)                              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│              Copilot Studio (Framework Copilot)                 │
│   ┌──────────────────────────┐  ┌───────────────────────────┐  │
│   │ Topics + Generative      │  │ Knowledge Sources (RAG)   │  │
│   │ Orchestration            │  │ SharePoint-hosted docs    │  │
│   └──────────┬───────────────┘  └───────────────────────────┘  │
└──────────────┼─────────────────────────┬───────────────────────┘
       reasoning                    workflows
               │                         │
┌──────────────▼───────────┐  ┌─────────▼─────────────────────┐
│  Azure Foundry Agent     │  │  Power Automate               │
│  GPT-4o · Python SDK     │  │  Provisioning · Approvals     │
└──────────────┬───────────┘  └──┬──────────┬─────────────────┘
               │                 │          │
┌──────────────▼───────────────────────────────────────────────┐
│              Azure Functions (Python)                         │
│  Learning path generation · Graph API calls · Cosmos logging │
└──────┬───────────────┬───────────────────┬───────────────────┘
       │               │                   │
┌──────▼──────┐ ┌──────▼──────┐ ┌─────────▼──────────────────┐
│ Cosmos DB   │ │ Dataverse   │ │ Microsoft Graph            │
│ Threads     │ │ Profiles    │ │ Users · Mail · AD · Cal    │
│ Sessions    │ │ Tickets     │ │                            │
│             │ │ Paths       │ │                            │
│             │ │ Audit Log   │ │                            │
└─────────────┘ └─────────────┘ └────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│           Monitoring & Analytics (Observability)            │
│  Copilot Studio  │  Application Insights  │  Foundry Ctrl  │
│  Analytics       │  OpenTelemetry Traces   │  Evaluators    │
│  Engagement      │  Latency · Tokens       │  Groundedness  │
│  CSAT · Topics   │  Error Rates · Cost     │  Safety        │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Conversational AI** | Microsoft Copilot Studio (generative orchestration + topics) |
| **LLM** | Azure AI Foundry Agent Service — GPT-4o |
| **Automation** | Power Automate (cloud flows + Teams Approvals) |
| **Integration** | Microsoft Graph (Azure AD, Outlook, Calendar) |
| **Knowledge Base** | SharePoint-hosted docs with Copilot Studio generative retrieval (RAG) |
| **Thread Storage** | Azure Cosmos DB (BYO thread storage for Foundry Agent Service) |
| **Business Data** | Microsoft Dataverse (profiles, access requests, learning paths, audit log) |
| **Custom Logic** | Azure Functions — Python 3.11 |
| **Observability** | Copilot Studio Analytics + Application Insights (OpenTelemetry) + Foundry Control Plane |
| **Deployment** | Microsoft Teams |

---

## Project Structure

```
onboarding-ai-buddy-copilot/
│
├── azure-functions/                    # Azure Functions (Python)
│   ├── GenerateLearningPath/
│   │   ├── __init__.py                 # Calls Foundry Agent for learning path generation
│   │   └── function.json               # HTTP trigger config
│   ├── LookupUserGraph/
│   │   ├── __init__.py                 # Microsoft Graph user lookup
│   │   └── function.json
│   ├── LogToCosmosDB/
│   │   ├── __init__.py                 # Session event logging to Cosmos DB
│   │   └── function.json
│   ├── host.json                       # Azure Functions host config
│   ├── local.settings.json             # Local dev environment variables
│   └── requirements.txt               # Python dependencies
│
├── foundry-agent/
│   ├── create_agent.py                 # Python script to create Foundry agent via SDK
│   └── agent_config.yaml              # Agent instructions and model config
│
├── knowledge-base/                     # Documents uploaded to SharePoint
│   ├── onboarding/
│   │   ├── day-1-checklist.md
│   │   ├── team-norms.md
│   │   ├── vpn-access.md
│   │   ├── access-provisioning-guide.md
│   │   ├── communication-channels.md
│   │   └── dev-environment-setup.md
│   ├── architecture/
│   │   ├── system-overview.md
│   │   ├── authentication-service.md
│   │   ├── payment-service.md
│   │   ├── data-pipeline.md
│   │   └── api-gateway.md
│   └── runbooks/
│       ├── deployment-guide.md
│       ├── incident-response.md
│       ├── monitoring-alerting.md
│       └── database-operations.md
│
├── infrastructure/
│   ├── deploy.sh                       # Azure CLI deployment script (all resources)
│   └── cleanup.sh                      # Tear down all Azure resources
│
├── copilot-studio/                     # Copilot Studio configuration (exported)
│   ├── topics/
│   │   ├── new-joiner-onboarding.yaml  # Main onboarding topic flow
│   │   ├── show-my-progress.yaml       # Progress tracking topic
│   │   └── mark-document-complete.yaml # Document completion topic
│   └── agent-instructions.md          # System prompt / agent instructions
│
├── power-automate/                     # Flow documentation and screenshots
│   ├── flow-1-provision-access.md      # Main provisioning flow design
│   ├── flow-2-send-welcome-email.md    # Welcome email + calendar invite
│   ├── flow-3-generate-learning-path.md # Learning path generation flow
│   └── flow-4-update-progress.md       # Progress update flow
│
├── dataverse/
│   └── schema.md                       # All 5 table schemas with column definitions
│
├── docs/
│   ├── architecture-diagram.png        # Architecture diagram
│   ├── demo-screenshots/               # Screenshots of running system
│   │   ├── teams-chat.png
│   │   ├── copilot-studio-topics.png
│   │   ├── power-automate-flows.png
│   │   ├── dataverse-tables.png
│   │   ├── cosmos-db-data-explorer.png
│   │   ├── analytics-dashboard.png
│   │   └── teams-approval.png
│   └── sample-conversation.md          # Example conversation transcript
│
├── .env.example                        # Environment variable template
├── .gitignore
├── LICENSE
└── README.md
```

---

## Sample Conversation

```
Developer: "Hi, I'm Maya Sehgal joining the Risk & Compliance team
            as a mid-level backend engineer"

Buddy:  Welcome Maya! Let me collect a few details to get you set up.
        → Asks for email, manager name
        → Confirms all details

        [Profile confirmed → auto-provisions:]
        ✅ 6 access tickets raised (GitHub, Jenkins, AWS, Snowflake, Datadog, Confluence)
        ✅ 4 DL subscription emails sent
        ✅ 3 AD group requests submitted
        ✅ Welcome email sent to maya@company.com
        ✅ Onboarding kickoff meeting created with manager
        ✅ Personalised 10-doc learning path generated

Developer: "How do I set up my VPN?"
Buddy:  Retrieves from SharePoint knowledge base → answers with source citation

Developer: "Mark the deployment guide as complete"
Buddy:  ✅ Updated in Dataverse. You have 9 items remaining.

Developer: "Show me my learning path"
Buddy:  Displays progress: 1/10 complete, next recommended: Incident Response Guide

Manager: [Receives Teams Approval] → Approves access requests
         → Status updated in Dataverse
```

---

## Prerequisites

| Requirement | Source | Cost |
|------------|--------|------|
| Azure Account | [azure.microsoft.com/free](https://azure.microsoft.com/free) | FREE ($200 credit) |
| M365 Business Basic Trial | [microsoft.com/microsoft-365](https://www.microsoft.com/microsoft-365/business/microsoft-365-business-basic) | FREE (1 month) |
| Copilot Studio Trial | [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) | FREE (60 days) |
| Python 3.11+ | [python.org](https://python.org) | FREE |
| Azure CLI | [learn.microsoft.com/cli/azure](https://learn.microsoft.com/cli/azure/install-azure-cli) | FREE |
| VS Code | [code.visualstudio.com](https://code.visualstudio.com) | FREE |

---

## Setup & Deployment

### 1. Azure Infrastructure

```bash
# Create resource group
az group create --name rg-onboarding-buddy --location eastus

# Create storage account
az storage account create --name onboardingbuddystore \
  --resource-group rg-onboarding-buddy --location eastus --sku Standard_LRS

# Create Cosmos DB
az cosmosdb create --name onboarding-buddy-cosmos \
  --resource-group rg-onboarding-buddy --default-consistency-level Session

# Create Cosmos DB database
az cosmosdb sql database create --account-name onboarding-buddy-cosmos \
  --resource-group rg-onboarding-buddy --name enterprise_memory

# Create Function App
az functionapp create --name onboarding-buddy-functions \
  --resource-group rg-onboarding-buddy --runtime python \
  --runtime-version 3.11 --functions-version 4 \
  --storage-account onboardingbuddystore \
  --consumption-plan-location eastus --os-type Linux

# Create Application Insights
az monitor app-insights component create \
  --app onboarding-buddy-insights --location eastus \
  --resource-group rg-onboarding-buddy --kind web
```

### 2. Deploy Azure Functions

```bash
cd azure-functions
pip install -r requirements.txt
func azure functionapp publish onboarding-buddy-functions
```

### 3. Create Foundry Agent

```bash
cd foundry-agent
python create_agent.py
```

### 4. Copilot Studio + Power Automate

Configured via browser-based portals:
- **Copilot Studio**: [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) — create agent, topics, connect knowledge sources
- **Power Automate**: [make.powerautomate.com](https://make.powerautomate.com) — build provisioning, email, and approval flows
- **SharePoint**: Upload knowledge base documents to your tenant's SharePoint site

### 5. Deploy to Teams

In Copilot Studio → Publish → Channels → Microsoft Teams → Turn on

---

## Cloud Deployment

All components run in the cloud. Nothing runs locally in production.

| Component | Platform | Endpoint |
|-----------|----------|----------|
| Copilot Studio Agent | Microsoft Power Platform (SaaS) | copilotstudio.microsoft.com |
| Teams Channel | Microsoft 365 (SaaS) | teams.microsoft.com |
| Azure Foundry Agent | Azure (your subscription) | *.services.ai.azure.com |
| Azure Functions | Azure (your subscription) | *.azurewebsites.net |
| Cosmos DB | Azure (your subscription) | *.documents.azure.com |
| Dataverse | Microsoft Power Platform (SaaS) | *.crm.dynamics.com |
| Power Automate | Microsoft Power Platform (SaaS) | make.powerautomate.com |
| Microsoft Graph | Microsoft 365 (SaaS) | graph.microsoft.com |
| Application Insights | Azure (your subscription) | *.applicationinsights.azure.com |

### Cleanup

```bash
az group delete --name rg-onboarding-buddy --yes --no-wait
```

---

## Monitoring & Observability

| Layer | Tool | Metrics |
|-------|------|---------|
| **Conversation** | Copilot Studio Analytics | Engagement rate, CSAT, resolution rates, topic performance, knowledge source usage |
| **Technical** | Application Insights (OpenTelemetry) | LLM call traces, latency, token usage, error rates, function execution logs |
| **AI Quality** | Foundry Control Plane | Groundedness, tool call accuracy, safety scores, continuous evaluation |
| **Governance** | Power Platform Admin Center | Capacity, content moderation, security |

---

## Environment Variables

```env
# Azure Foundry
FOUNDRY_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>

# Cosmos DB
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
COSMOS_KEY=<your-cosmos-key>

# Application Insights
APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=<key>;IngestionEndpoint=...

# Microsoft Graph (App Registration)
GRAPH_CLIENT_ID=<app-id>
GRAPH_TENANT_ID=<tenant-id>
GRAPH_CLIENT_SECRET=<secret>
```

---

## Author

**Sneh Dehmiwal**
AI & ML Engineering Leader | Technical Product Leadership
Building production-grade agentic AI systems

[LinkedIn](https://www.linkedin.com/in/snehdehmiwal/) · [GitHub](https://github.com/SanehLata) · [Portfolio](https://sanehlata.github.io)
