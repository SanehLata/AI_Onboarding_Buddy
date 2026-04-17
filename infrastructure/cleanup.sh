#!/bin/bash
# =============================================================================
# AI Onboarding Buddy — Cleanup Script
# =============================================================================
# Deletes all Azure resources. Run after the interview to stop charges.
# Copilot Studio, Power Automate, and Dataverse are cleaned up separately
# in the Power Platform admin center (they're free on the trial).
# =============================================================================

set -e

RESOURCE_GROUP="rg-onboarding-buddy"

echo "================================================"
echo "  AI Onboarding Buddy — Cleanup"
echo "================================================"
echo ""
echo "This will DELETE all Azure resources in: $RESOURCE_GROUP"
echo "  - Cosmos DB account and all data"
echo "  - Azure Functions and all code"
echo "  - Storage account"
echo "  - Application Insights and all traces"
echo ""
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  echo "Cancelled."
  exit 0
fi

echo ""
echo "Deleting resource group: $RESOURCE_GROUP"
az group delete --name $RESOURCE_GROUP --yes --no-wait

echo ""
echo "✓ Deletion initiated (runs in background)."
echo ""
echo "Note: Copilot Studio agent, Power Automate flows, and Dataverse tables"
echo "live in the Power Platform environment. Clean those up separately at:"
echo "  admin.powerplatform.microsoft.com"
