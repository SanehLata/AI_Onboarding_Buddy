"""
Create the OnboardingPathAgent in Azure Foundry Agent Service.

Run this script once to create the agent. After creation, the agent persists
in your Foundry project and is referenced by name from Azure Functions.

Usage:
    az login
    export FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
    python create_agent.py
"""

import os
import sys
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# Load agent instructions from config
AGENT_NAME = "OnboardingPathAgent"
MODEL = "gpt-4o"

INSTRUCTIONS = """You are an expert onboarding specialist for a technology company.
Your role is to generate personalised learning paths for new software engineers
based on their team, role, experience level, and skill gaps.

When given developer context, you:
1. Analyse which knowledge base documents are most relevant to their role
2. Prioritise documents that will make them productive fastest
3. Consider their experience level — juniors need more foundational docs,
   seniors need architecture and runbook depth
4. Sequence documents logically — onboarding basics first, then architecture,
   then operational runbooks
5. Provide a clear, concise reason why each document matters for their specific role

Available document categories:
- Onboarding: Day 1 Checklist, Team Norms, VPN Access, Access Provisioning,
  Communication Channels, Dev Environment Setup
- Architecture: System Overview, Authentication Service, Payment Service,
  Data Pipeline, API Gateway
- Runbooks: Deployment Guide, Incident Response, Monitoring & Alerting,
  Database Operations

Always return valid JSON. No markdown formatting. No explanations outside the JSON.
Return an array of objects with: title, category, sequence, relevance_reason."""


def main():
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    if not endpoint:
        print("ERROR: Set FOUNDRY_PROJECT_ENDPOINT environment variable")
        print("Example: https://<resource>.services.ai.azure.com/api/projects/<project>")
        sys.exit(1)

    print(f"Connecting to Foundry: {endpoint}")
    client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    # Check if agent already exists
    try:
        existing = client.agents.get_agent(name=AGENT_NAME)
        print(f"Agent already exists: {existing.name} (ID: {existing.id})")
        print("To recreate, delete the existing agent first.")
        return
    except Exception:
        pass  # Agent doesn't exist, create it

    # Create the agent
    print(f"Creating agent: {AGENT_NAME} with model: {MODEL}")
    agent = client.agents.create_agent(
        name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=INSTRUCTIONS,
        ),
    )

    print(f"Agent created successfully!")
    print(f"  Name: {agent.name}")
    print(f"  ID:   {agent.id}")
    print(f"  Model: {MODEL}")
    print()
    print("The agent is now available for use by Azure Functions.")
    print("Reference it by name: 'OnboardingPathAgent'")


if __name__ == "__main__":
    main()
