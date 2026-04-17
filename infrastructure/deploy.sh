#!/bin/bash
# =============================================================================
# AI Onboarding Buddy — Azure Infrastructure Deployment
# =============================================================================
# This script creates all Azure resources needed for the project.
# Run once to set up the infrastructure. Idempotent — safe to re-run.
#
# Prerequisites:
#   - Azure CLI installed and authenticated (az login)
#   - Azure subscription with $200 free credit
#
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh
# =============================================================================

set -e

RESOURCE_GROUP="rg-onboarding-buddy"
LOCATION="eastus"
COSMOS_ACCOUNT="onboarding-buddy-cosmos"
COSMOS_DB="enterprise_memory"
STORAGE_ACCOUNT="onboardingbuddystore"
FUNCTION_APP="onboarding-buddy-functions"
APP_INSIGHTS="onboarding-buddy-insights"

echo "================================================"
echo "  AI Onboarding Buddy — Azure Deployment"
echo "================================================"
echo ""

# 1. Resource Group
echo "[1/6] Creating resource group: $RESOURCE_GROUP"
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION \
  --output none
echo "  ✓ Resource group ready"

# 2. Storage Account (required by Azure Functions)
echo "[2/6] Creating storage account: $STORAGE_ACCOUNT"
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS \
  --output none
echo "  ✓ Storage account ready"

# 3. Cosmos DB Account + Database
echo "[3/6] Creating Cosmos DB account: $COSMOS_ACCOUNT"
az cosmosdb create \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --kind GlobalDocumentDB \
  --default-consistency-level Session \
  --output none
echo "  ✓ Cosmos DB account ready"

echo "  Creating database: $COSMOS_DB"
az cosmosdb sql database create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --name $COSMOS_DB \
  --output none
echo "  ✓ Database ready"

echo "  Creating container: onboarding_sessions"
az cosmosdb sql container create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --database-name $COSMOS_DB \
  --name onboarding_sessions \
  --partition-key-path /developer_id \
  --output none
echo "  ✓ Container ready"

# 4. Azure Function App
echo "[4/6] Creating Function App: $FUNCTION_APP"
az functionapp create \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --storage-account $STORAGE_ACCOUNT \
  --consumption-plan-location $LOCATION \
  --os-type Linux \
  --output none
echo "  ✓ Function App ready"

# 5. Application Insights
echo "[5/6] Creating Application Insights: $APP_INSIGHTS"
az monitor app-insights component create \
  --app $APP_INSIGHTS \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --kind web \
  --output none
echo "  ✓ Application Insights ready"

# 6. Retrieve connection details
echo "[6/6] Retrieving connection details..."
echo ""

COSMOS_ENDPOINT=$(az cosmosdb show \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query documentEndpoint \
  --output tsv)

COSMOS_KEY=$(az cosmosdb keys list \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query primaryMasterKey \
  --output tsv)

INSIGHTS_KEY=$(az monitor app-insights component show \
  --app $APP_INSIGHTS \
  --resource-group $RESOURCE_GROUP \
  --query connectionString \
  --output tsv)

echo "================================================"
echo "  Deployment Complete!"
echo "================================================"
echo ""
echo "Add these to your Azure Function App configuration:"
echo ""
echo "  COSMOS_ENDPOINT=$COSMOS_ENDPOINT"
echo "  COSMOS_KEY=$COSMOS_KEY"
echo "  APPINSIGHTS_CONNECTION_STRING=$INSIGHTS_KEY"
echo ""
echo "Next steps:"
echo "  1. Create Azure Foundry project in the portal"
echo "  2. Deploy GPT-4o model in the Foundry project"
echo "  3. Run: python foundry-agent/create_agent.py"
echo "  4. Deploy functions: cd azure-functions && func azure functionapp publish $FUNCTION_APP"
echo "  5. Configure Copilot Studio and Power Automate in the browser"
echo ""
echo "To tear down everything: ./cleanup.sh"
