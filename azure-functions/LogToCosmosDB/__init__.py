import azure.functions as func
import json
import os
import logging
from datetime import datetime, timezone
from azure.cosmos import CosmosClient, PartitionKey
from opentelemetry import trace

tracer = trace.get_tracer("onboarding-buddy")
logger = logging.getLogger("LogToCosmosDB")

# Lazy-initialised client (reused across invocations)
_cosmos_client = None
_container = None


def _get_container():
    """Get or create the Cosmos DB container client (singleton)."""
    global _cosmos_client, _container
    if _container is None:
        _cosmos_client = CosmosClient(
            os.environ["COSMOS_ENDPOINT"],
            os.environ["COSMOS_KEY"],
        )
        db = _cosmos_client.get_database_client("enterprise_memory")
        _container = db.get_container_client("onboarding_sessions")
    return _container


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Logs onboarding session events to Azure Cosmos DB.
    Used for session tracking, progress auditing, and cross-reference
    with Dataverse records.

    Called by Power Automate flows after provisioning, email, and
    learning path actions.

    Input JSON:
        {
            "session_id": "session-abc-123",
            "developer_id": "dev-001",
            "event_type": "PROFILE_CREATED | TICKET_RAISED | EMAIL_SENT |
                           PATH_GENERATED | APPROVAL_SENT | DOC_COMPLETED",
            "details": {
                "action": "Created developer profile",
                "team": "Risk & Compliance",
                "tickets_count": 6
            }
        }

    Returns:
        { "status": "logged", "id": "<cosmos-document-id>" }
    """
    with tracer.start_as_current_span("log_to_cosmos") as span:
        try:
            data = req.get_json()

            session_id = data["session_id"]
            developer_id = data["developer_id"]
            event_type = data["event_type"]
            details = data.get("details", {})

            span.set_attribute("developer_id", developer_id)
            span.set_attribute("event_type", event_type)

            # Build the Cosmos DB document
            timestamp = datetime.now(timezone.utc).isoformat()
            doc_id = f"{session_id}-{event_type}-{timestamp}"

            document = {
                "id": doc_id,
                "session_id": session_id,
                "developer_id": developer_id,
                "event_type": event_type,
                "timestamp": timestamp,
                "details": details,
            }

            # Upsert to Cosmos DB
            container = _get_container()
            result = container.upsert_item(document)

            logger.info(
                f"[COSMOS_LOG] logged event — dev_id={developer_id} "
                f"event={event_type} doc_id={doc_id}"
            )

            return func.HttpResponse(
                json.dumps({"status": "logged", "id": result["id"]}),
                mimetype="application/json",
                status_code=200,
            )

        except KeyError as e:
            logger.error(f"[COSMOS_LOG] missing required field: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": f"Missing required field: {str(e)}"}),
                mimetype="application/json",
                status_code=400,
            )
        except Exception as e:
            logger.error(f"[COSMOS_LOG] error: {str(e)}")
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            return func.HttpResponse(
                json.dumps({"error": "Failed to log event", "details": str(e)}),
                mimetype="application/json",
                status_code=500,
            )
