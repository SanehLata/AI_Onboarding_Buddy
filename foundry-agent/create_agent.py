"""
Create the OnboardingPathAgent in Azure Foundry Agent Service.

Run this script once to create the agent. After creation, the agent persists
in your Foundry project and is referenced by ID from Azure Functions.

Usage:
    set FOUNDRY_API_KEY=<your-api-key>
    set FOUNDRY_API_BASE=<your-endpoint>
    python create_agent.py

Or pass values directly in the script for first-time setup.
"""

import os
import sys
from openai import AzureOpenAI

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
    api_key = os.environ.get("FOUNDRY_API_KEY")
    api_base = os.environ.get("FOUNDRY_API_BASE")

    if not api_key or not api_base:
        print("ERROR: Set environment variables:")
        print("  set FOUNDRY_API_KEY=<your-api-key>")
        print("  set FOUNDRY_API_BASE=<your-cognitive-services-endpoint>")
        print("Example: https://onboarding-buddy-foundry.cognitiveservices.azure.com/")
        sys.exit(1)

    print(f"Connecting to: {api_base}")

    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=api_base,
        api_version="2025-01-01-preview",
    )

    # Check if agent already exists
    existing_agents = client.beta.assistants.list()
    for agent in existing_agents.data:
        if agent.name == AGENT_NAME:
            print(f"Agent already exists: {agent.name} (ID: {agent.id})")
            print("To recreate, delete the existing agent first.")
            return

    # Create the agent
    print(f"Creating agent: {AGENT_NAME} with model: {MODEL}")
    agent = client.beta.assistants.create(
        name=AGENT_NAME,
        model=MODEL,
        instructions=INSTRUCTIONS,
        temperature=0.3,
    )

    print(f"\nAgent created successfully!")
    print(f"  Name: {agent.name}")
    print(f"  ID:   {agent.id}")
    print(f"  Model: {MODEL}")
    print()
    print("Add this to your Azure Function App environment variables:")
    print(f"  FOUNDRY_AGENT_ID={agent.id}")
    print()
    print("The agent is now available for use by Azure Functions.")


if __name__ == "__main__":
    main()