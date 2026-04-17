# Flow 4: Update Progress

## Overview
Updates a learning path item status to "Complete" when the developer marks a document as finished.

## Configuration
- **Trigger**: "Run a flow from Copilot"
- **Inputs**: DeveloperEmail (text), DocumentTitle (text)
- **Returns**: Confirmation text with remaining count

## Steps

### Step 1: Find Developer Profile
- **Action**: Dataverse — List rows
- **Table**: Developer Profile
- **Filter**: Email eq '{DeveloperEmail}'
- **Save**: DeveloperProfileId

### Step 2: Find Learning Path Item
- **Action**: Dataverse — List rows
- **Table**: Learning Path Item
- **Filter**: Developer eq '{DeveloperProfileId}' AND Document Title contains '{DocumentTitle}'
- **Save**: LearningPathItemId

### Step 3: Condition — Item Found?
- **Yes** → Continue to Step 4
- **No** → Return: "I couldn't find a document matching '{DocumentTitle}' in your learning path. Can you check the title?"

### Step 4: Update Status
- **Action**: Dataverse — Update a row
- **Table**: Learning Path Item
- **Row ID**: LearningPathItemId
- **Set**: Status = "Complete"

### Step 5: Count Remaining
- **Action**: Dataverse — List rows
- **Table**: Learning Path Item
- **Filter**: Developer eq '{DeveloperProfileId}' AND Status ne 'Complete'
- **Save**: RemainingCount = length of results

### Step 6: Find Next Document
- **Action**: Dataverse — List rows
- **Table**: Learning Path Item
- **Filter**: Developer eq '{DeveloperProfileId}' AND Status eq 'Not Started'
- **Sort**: Sequence ascending
- **Top**: 1
- **Save**: NextDocumentTitle

### Step 7: Log to Audit Trail
- **Action**: Dataverse — Add a new row
- **Table**: Agent Action Log
- **Type**: DOC_COMPLETED
- **Details**: "{DocumentTitle} marked complete"

### Step 8: Return
- **Output**: "✅ Marked '{DocumentTitle}' as complete! You have {RemainingCount} items remaining. Next recommended: {NextDocumentTitle}"
