import azure.functions as func
import json
import os
import logging
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from opentelemetry import trace

tracer = trace.get_tracer("onboarding-buddy")
logger = logging.getLogger("LookupUserGraph")


def _get_graph_client() -> GraphServiceClient:
    """Create an authenticated Microsoft Graph client using app credentials."""
    credential = ClientSecretCredential(
        tenant_id=os.environ["GRAPH_TENANT_ID"],
        client_id=os.environ["GRAPH_CLIENT_ID"],
        client_secret=os.environ["GRAPH_CLIENT_SECRET"],
    )
    return GraphServiceClient(credential)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Looks up a user in Azure AD via Microsoft Graph API.
    Returns user profile details including ID, display name, department,
    job title, and manager information.

    Called by Power Automate Flow 1 (Provision Access) and Azure Functions
    internally for manager validation.

    Input JSON:
        {
            "email": "maya.sehgal@company.com"
        }

    Returns:
        {
            "id": "azure-ad-user-id",
            "displayName": "Maya Sehgal",
            "email": "maya.sehgal@company.com",
            "department": "Risk & Compliance",
            "jobTitle": "Backend Engineer",
            "manager": {
                "id": "manager-ad-id",
                "displayName": "James Thornton",
                "email": "james.thornton@company.com"
            }
        }
    """
    with tracer.start_as_current_span("lookup_user_graph") as span:
        try:
            data = req.get_json()
            email = data["email"]

            span.set_attribute("lookup_email", email)
            logger.info(f"[GRAPH_LOOKUP] looking up user: {email}")

            client = _get_graph_client()

            # Look up user by email (userPrincipalName)
            user = client.users.by_user_id(email).get()

            result = {
                "id": user.id,
                "displayName": user.display_name,
                "email": email,
                "department": user.department,
                "jobTitle": user.job_title,
            }

            # Try to get manager details
            try:
                manager = client.users.by_user_id(email).manager.get()
                result["manager"] = {
                    "id": manager.id,
                    "displayName": manager.display_name,
                    "email": getattr(manager, "user_principal_name", None),
                }
                logger.info(
                    f"[GRAPH_LOOKUP] found manager: {manager.display_name}"
                )
            except Exception as e:
                logger.warning(f"[GRAPH_LOOKUP] manager not found: {str(e)}")
                result["manager"] = None

            span.set_attribute("user_found", True)
            span.set_attribute("department", user.department or "unknown")
            logger.info(
                f"[GRAPH_LOOKUP] success — user={user.display_name} "
                f"dept={user.department}"
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
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            return func.HttpResponse(
                json.dumps({"error": "User lookup failed", "details": str(e)}),
                mimetype="application/json",
                status_code=500,
            )
