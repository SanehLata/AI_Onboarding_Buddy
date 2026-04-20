import azure.functions as func
import json
import os
import logging
from openai import AzureOpenAI

logger = logging.getLogger("GenerateLearningPath")


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        team = data["team"]
        role = data["role"]
        level = data["experience_level"]
        skills = data.get("required_skills", "")
        developer_id = data.get("developer_id", "unknown")

        logger.info(
            f"[GENERATE_PATH] entry — dev_id={developer_id} "
            f"team={team} role={role} level={level}"
        )

        openai_client = AzureOpenAI(
            api_key=os.environ["FOUNDRY_API_KEY"],
            azure_endpoint=os.environ["FOUNDRY_API_BASE"],
            api_version="2025-01-01-preview",
        )

        agent_id = os.environ["FOUNDRY_AGENT_ID"]

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

        thread = openai_client.beta.threads.create()

        openai_client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=prompt
        )

        run = openai_client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=agent_id
        )

        messages = openai_client.beta.threads.messages.list(thread_id=thread.id)

        result_text = ""
        for msg in messages.data:
            if msg.role == "assistant":
                result_text = msg.content[0].text.value
                break

        clean_text = result_text.strip()
        if clean_text.startswith("```"):
            clean_text = clean_text.split("\n", 1)[1]
        if clean_text.endswith("```"):
            clean_text = clean_text.rsplit("```", 1)[0]
        clean_text = clean_text.strip()

        learning_path = json.loads(clean_text)

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
        return func.HttpResponse(
            json.dumps({"error": "Internal server error", "details": str(e)}),
            mimetype="application/json",
            status_code=500,
        )