# Flow 2: Send Welcome Email + Calendar Invite

## Overview
Sends a real Outlook welcome email and creates an onboarding kickoff meeting with the developer's manager via Microsoft Graph.

## Configuration
- **Trigger**: "Run a flow from Copilot"
- **Inputs**: Email (text), FullName (text), Team (text), ManagerEmail (text)
- **Returns**: Confirmation text

## Steps

### Step 1: Send Welcome Email
- **Action**: Office 365 Outlook — Send an email (V2)
- **To**: {Email}
- **Subject**: "Welcome to TechCorp, {FullName}! 🎉"
- **Body** (HTML):
  ```html
  <h2>Welcome to the {Team} team!</h2>
  <p>Hi {FullName},</p>
  <p>We're excited to have you on board. Your system access is being provisioned
  and you'll receive confirmation emails shortly.</p>
  <h3>Quick Links</h3>
  <ul>
    <li><a href="https://confluence.techcorp.com">Confluence Wiki</a></li>
    <li><a href="https://github.techcorp.com">GitHub Enterprise</a></li>
    <li><a href="https://servicenow.techcorp.com">ServiceNow Portal</a></li>
  </ul>
  <p>Your AI Onboarding Buddy has generated a personalised learning path for you.
  Open Teams and chat with the Onboarding Buddy to see it.</p>
  <p>Best,<br>TechCorp Engineering</p>
  ```

### Step 2: Create Calendar Invite
- **Action**: Office 365 Outlook — Create event (V4)
- **Calendar**: Default calendar
- **Subject**: "Onboarding Kickoff — {FullName}"
- **Start**: Tomorrow at 10:00 AM (dynamic expression)
- **End**: Tomorrow at 10:30 AM
- **Attendees**: {Email}; {ManagerEmail}
- **Body**: "Welcome meeting for {FullName} joining the {Team} team. Agenda: introductions, team overview, first-week goals."

### Step 3: Log Actions
- **Action**: Dataverse — Add a new row
- **Table**: Agent Action Log
- **Type**: WELCOME_EMAIL_SENT, status = Success
- **Action**: Dataverse — Add a new row
- **Type**: CALENDAR_INVITE_CREATED, status = Success

### Step 4: Return
- **Output**: "✅ Welcome email sent to {Email} and onboarding kickoff meeting created with {ManagerEmail} for tomorrow at 10:00 AM."
