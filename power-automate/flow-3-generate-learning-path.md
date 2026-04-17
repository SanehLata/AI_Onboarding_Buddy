# Flow 3: Generate Learning Path

## Overview
Calls the Azure Function (which internally calls the Foundry Agent) to generate a personalised learning path, then persists the items to Dataverse.

## Configuration
- **Trigger**: "Run a flow from Copilot"
- **Inputs**: Team (text), Role (text), ExperienceLevel (text), DeveloperProfileId (text), RequiredSkills (text)
- **Returns**: Formatted learning path text

## Steps

### Step 1: Call Azure Function — GenerateLearningPath
- **Action**: HTTP — POST
- **URL**: `https://onboarding-buddy-functions.azurewebsites.net/api/GenerateLearningPath`
- **Body**:
  ```json
  {
    "team": "{Team}",
    "role": "{Role}",
    "experience_level": "{ExperienceLevel}",
    "required_skills": "{RequiredSkills}",
    "developer_id": "{DeveloperProfileId}"
  }
  ```
- **Save**: Response body as `LearningPathJSON`

### Step 2: Parse JSON
- **Action**: Data Operations — Parse JSON
- **Content**: `LearningPathJSON`
- **Schema**: Array of { title, category, sequence, relevance_reason }

### Step 3: Create Dataverse Records
- **Action**: Apply to each (loop over parsed items)
  - **Action**: Dataverse — Add a new row
  - **Table**: Learning Path Item
  - **Map**:
    - Document Title = item.title
    - Developer = DeveloperProfileId (lookup)
    - Sequence = item.sequence
    - Category = item.category
    - Status = "Not Started"
    - Relevance Reason = item.relevance_reason

### Step 4: Log to Cosmos DB
- **Action**: HTTP — POST to LogToCosmosDB function
- **Event type**: PATH_GENERATED
- **Details**: Include full learning path and document count

### Step 5: Log to Audit Trail
- **Action**: Dataverse — Add a new row
- **Table**: Agent Action Log
- **Type**: PATH_GENERATED, status = Success
- **Details**: "{count} documents generated for {Team} {Role}"

### Step 6: Format and Return
- **Action**: Compose — Build formatted text
- **Output**:
  ```
  📚 Your Personalised Learning Path ({count} documents):

  1. {title} ({category}) — {relevance_reason}
  2. {title} ({category}) — {relevance_reason}
  ...

  Start with document 1 and work your way through. Ask me any questions as you go!
  ```
