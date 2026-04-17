# Flow 1: Provision Access (Main Provisioning Flow)

## Overview
The primary workflow that creates the developer profile and provisions all system access.

## Configuration
- **Trigger**: "Run a flow from Copilot"
- **Inputs**: FullName (text), Email (text), Team (text), Role (text), ExperienceLevel (text), ManagerEmail (text)
- **Returns**: Summary text (e.g., "Created 6 tickets, 4 DL subscriptions, 3 AD group requests")

## Steps

### Step 1: Create Developer Profile
- **Action**: Dataverse — Add a new row
- **Table**: Developer Profile
- **Map**: FullName → Full Name, Email → Email, Team → Team, Role → Role, ExperienceLevel → Experience Level, ManagerEmail → Manager Email
- **Set**: Onboarding Status = "In Progress"
- **Save**: Store the created record ID as `DeveloperProfileId`

### Step 2: Lookup User in Azure AD
- **Action**: HTTP — Call Azure Function `LookupUserGraph`
- **URL**: `https://onboarding-buddy-functions.azurewebsites.net/api/LookupUserGraph`
- **Body**: `{ "email": "{Email}" }`
- **Save**: Store Graph User ID from response
- **Update**: Dataverse Developer Profile → set Graph User ID

### Step 3: Lookup Team Configuration
- **Action**: Dataverse — List rows
- **Table**: Team Configuration
- **Filter**: Team Name eq '{Team}'
- **Save**: Required Systems, DL Groups, AD Groups from the result

### Step 4: Create Access Request — Tickets
- **Action**: Apply to each (loop over Required Systems, split by comma)
  - **Action**: Dataverse — Add a new row
  - **Table**: Access Request
  - **Map**: Developer = DeveloperProfileId, System Name = current item, Request Type = "Jira Ticket", Status = "Pending"
  - **Set**: Ticket ID = "TKT-" + rand(10000, 99999)
  - **Increment**: ticket counter

### Step 5: Create Access Request — DL Subscriptions
- **Action**: Apply to each (loop over DL Groups)
  - **Action**: Dataverse — Add a new row
  - **Table**: Access Request
  - **Map**: Request Type = "DL Subscription", Status = "Pending"

### Step 6: Create Access Request — AD Groups
- **Action**: Apply to each (loop over AD Groups)
  - **Action**: Dataverse — Add a new row
  - **Table**: Access Request
  - **Map**: Request Type = "AD Group", Status = "Pending"

### Step 7: Log Actions to Audit Trail
- **Action**: Dataverse — Add a new row (for each action type)
- **Table**: Agent Action Log
- **Types**: PROFILE_CREATED, TICKET_RAISED (x N), DL_SUB_SENT (x N), AD_GROUP_REQUESTED (x N)

### Step 8: Log to Cosmos DB
- **Action**: HTTP — Call Azure Function `LogToCosmosDB`
- **Body**: session event with provisioning summary

### Step 9: Return Summary
- **Output**: "✅ Created {ticket_count} access tickets, {dl_count} DL subscriptions, {ad_count} AD group requests. All requests are pending. Your manager will receive an approval request shortly."
