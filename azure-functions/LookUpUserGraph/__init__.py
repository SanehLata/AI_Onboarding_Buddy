import azure.functions as func
import json
import os
import logging
import asyncio
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

logger = logging.getLogger("LookupUserGraph")


def _get_graph_client() -> GraphServiceClient:
    credential = ClientSecretCredential(
        tenant_id=os.environ["GRAPH_TENANT_ID"],
        client_id=os.environ["GRAPH_CLIENT_ID"],
        client_secret=os.environ["GRAPH_CLIENT_SECRET"],
    )
    return GraphServiceClient(credential)


async def _lookup_user(email: str) -> dict:
    client = _get_graph_client()

    user = await client.users.by_user_id(email).get()

    result = {
        "id": user.id,
        "displayName": user.display_name,
        "email": email,
        "department": user.department,
        "jobTitle": user.job_title,
    }

    try:
        manager = await client.users.by_user_id(email).manager.get()
        result["manager"] = {
            "id": manager.id,
            "displayName": manager.display_name,
            "email": getattr(manager, "user_principal_name", None),
        }
        logger.info(f"[GRAPH_LOOKUP] found manager: {manager.display_name}")
    except Exception as e:
        logger.warning(f"[GRAPH_LOOKUP] manager not found: {str(e)}")
        result["manager"] = None

    return result


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        email = data["email"]

        logger.info(f"[GRAPH_LOOKUP] looking up user: {email}")

        result = asyncio.run(_lookup_user(email))

        logger.info(
            f"[GRAPH_LOOKUP] success — user={result.get('displayName')} "
            f"dept={result.get('department')}"
        )

        return func.HttpResponse(
            json.dumps(result, indent=2),
            mimetype="application/json",
            status_code=200,
        )

    except KeyError:
        return func.HttpResponse(
            json.dumps({"error": "Missing required field: email"}),
            mimetype="application/json",
            status_code=400,
        )
    except Exception as e:
        logger.error(f"[GRAPH_LOOKUP] error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "User lookup failed", "details": str(e)}),
            mimetype="application/json",
            status_code=500,
        )