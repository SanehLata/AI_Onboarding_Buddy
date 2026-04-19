import azure.functions as func
import json
import os
import logging
from datetime import datetime, timezone
from azure.cosmos import CosmosClient

logger = logging.getLogger("LogToCosmosDB")

_cosmos_client = None
_container = None


def _get_container():
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
    try:
        data = req.get_json()

        session_id = data["session_id"]
        developer_id = data["developer_id"]
        event_type = data["event_type"]
        details = data.get("details", {})

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
        return func.HttpResponse(
            json.dumps({"error": "Failed to log event", "details": str(e)}),
            mimetype="application/json",
            status_code=500,
        )