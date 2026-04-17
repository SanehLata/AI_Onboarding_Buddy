import azure.functions as func
import json
import os
import logging
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Configure observability
if os.environ.get("APPINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor(
        connection_string=os.environ["APPINSIGHTS_CONNECTION_STRING"]
    )

tracer = trace.get_tracer("onboarding-buddy")
logger = logging.getLogger("GenerateLearningPath")


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Generates a personalised learning path for a new developer by calling
    the Azure Foundry Agent (GPT-4o) with team, role, and skill context.

    Called by Power Automate Flow 3 (Generate Learning Path).

    Input JSON:
        {
            "team": "Risk & Compliance",
            "role": "Backend Engineer",
            "experience_level": "mid",
            "required_skills": "Python, SQL, Spark, Risk Modelling",
            "developer_id": "dev-001"
        }

    Returns JSON array of learning path items:
        [
            {
                "title": "Day 1 Checklist",
                "category": "Onboarding",
                "sequence": 1,
                "relevance_reason": "Essential first-day orientation for all new joiners"
            },
            ...
        ]
    """
    with tracer.start_as_current_span("generate_learning_path") as span:
        try:
            data = req.get_json()
            team = data["team"]
            role = data["role"]
            level = data["experience_level"]
            skills = data.get("required_skills", "")
            developer_id = data.get("developer_id", "unknown")

            span.set_attribute("developer_id", developer_id)
            span.set_attribute("team", team)
            span.set_attribute("role", role)
            span.set_attribute("experience_level", level)

            logger.info(
                f"[GENERATE_PATH] entry — dev_id={developer_id} "
                f"team={team} role={role} level={level}"
            )

            # Connect to Azure Foundry Agent Service
            client = AIProjectClient(
                endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                credential=DefaultAzureCredential(),
            )

            # Get the pre-created onboarding agent
            agent = client.agents.get_agent(name="OnboardingPathAgent")
            logger.info(f"[GENERATE_PATH] using agent: {agent.name} (ID: {agent.id})")

            # Create a conversation thread
            thread = client.agents.threads.create()

            # Build the prompt with developer context
            prompt = f"""Generate a personalised learning path for a new developer with these details:
- Team: {team}
- Role: {role}
- Experience Level: {level}
- Skills needed: {skills}

Available knowledge base documents by category:

ONBOARDING:
- Day 1 Checklist
- Team Norms and Culture
- VPN Access Setup
- Access Provisioning Guide
- Communication Channels
- Development Environment Setup

ARCHITECTURE:
- System Overview
- Authentication Service
- Payment Service
- Data Pipeline
- API Gateway

RUNBOOKS:
- Deployment Guide
- Incident Response
- Monitoring and Alerting
- Database Operations

Select 8-10 documents most relevant to this developer's role and team.
Order them by priority — what they should read first to be productive fastest.

Return ONLY a valid JSON array with these fields for each item:
- title (exact document name from the list above)
- category (Onboarding / Architecture / Runbooks)
- sequence (1, 2, 3... in reading order)
- relevance_reason (one sentence explaining why this matters for their role)

Return ONLY the JSON array, no markdown formatting, no explanation."""

            # Send the prompt to the agent
            client.agents.messages.create(
                thread_id=thread.id, role="user", content=prompt
            )

            # Run the agent and wait for completion
            run = client.agents.runs.create_and_wait(
                thread_id=thread.id, agent_id=agent.id
            )

            # Retrieve the response
            messages = client.agents.messages.list(thread_id=thread.id)
            result_text = messages.data[0].content[0].text.value

            # Parse and validate the JSON response
            # Strip markdown code fences if present
            clean_text = result_text.strip()
            if clean_text.startswith("```"):
                clean_text = clean_text.split("\n", 1)[1]
            if clean_text.endswith("```"):
                clean_text = clean_text.rsplit("```", 1)[0]
            clean_text = clean_text.strip()

            learning_path = json.loads(clean_text)

            span.set_attribute("documents_generated", len(learning_path))
            logger.info(
                f"[GENERATE_PATH] success — dev_id={developer_id} "
                f"doc_count={len(learning_path)}"
            )

            return func.HttpResponse(
                json.dumps(learning_path, indent=2),
                mimetype="application/json",
                status_code=200,
            )

        except json.JSONDecodeError as e:
            logger.error(f"[GENERATE_PATH] JSON parse error: {str(e)}")
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            return func.HttpResponse(
                json.dumps({"error": "Failed to parse learning path from LLM", "details": str(e)}),
                mimetype="application/json",
                status_code=500,
            )
        except KeyError as e:
            logger.error(f"[GENERATE_PATH] Missing required field: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": f"Missing required field: {str(e)}"}),
                mimetype="application/json",
                status_code=400,
            )
        except Exception as e:
            logger.error(f"[GENERATE_PATH] unexpected error: {str(e)}")
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            return func.HttpResponse(
                json.dumps({"error": "Internal server error", "details": str(e)}),
                mimetype="application/json",
                status_code=500,
            )
