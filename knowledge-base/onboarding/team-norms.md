# Team Norms and Culture

## Working Hours
Core collaboration hours are 10:00 AM - 4:00 PM EST. Outside these hours, work asynchronously. No expectation to respond to Slack messages after 6:00 PM unless you're on-call.

## Communication Channels
- **Slack** for day-to-day communication. Use threads for discussions.
- **Email** for external stakeholders and formal communications.
- **Teams** for scheduled meetings and video calls.
- Avoid DMs for technical discussions — keep them in team channels so knowledge is shared.

## Code Review Standards
- All PRs require at least 2 approvals before merge.
- Reviewers should respond within 4 business hours.
- Use conventional comments: prefix with `nit:`, `question:`, `suggestion:`, or `blocker:`.
- Keep PRs under 400 lines of changes. Split larger work into stacked PRs.

## Meeting Culture
- All meetings must have an agenda shared 24 hours in advance.
- Default meeting length is 25 minutes (not 30) to allow transition time.
- Cameras on for standups and team meetings. Optional for focus sessions.
- No-meeting blocks: Wednesday afternoons are protected focus time.

## On-Call Rotation
- Each team member is on-call for one week every 6 weeks.
- On-call engineer responds to PagerDuty alerts within 15 minutes during business hours, 30 minutes after hours.
- Refer to the Incident Response runbook for escalation procedures.

## Sprint Cadence
- 2-week sprints, starting on Mondays.
- Sprint Planning: Monday 10:00 AM.
- Daily Standup: 10:15 AM (15 minutes max).
- Sprint Review: Friday 2:00 PM (every other week).
- Retrospective: Friday 3:00 PM (every other week).

## Definition of Done
A story is done when:
1. Code is merged to main with passing CI/CD pipeline.
2. Unit test coverage is above 80% for new code.
3. Integration tests pass in the staging environment.
4. Documentation is updated (API docs, runbooks, or architecture diagrams as applicable).
5. Product Owner has accepted the story in the sprint review.
