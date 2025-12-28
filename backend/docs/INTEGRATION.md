## Frontend Integration Guide

### Message Send (per-partner private chat)
POST `/messages`
```json
{
  "conversation_id": "<uuid>",
  "user_id": "<uuid>",
  "content": "I felt anxious last night..."
}
```
Response includes assistant reply IDs and content. Store conversation_id per user; create one via POST `/conversations`.

### History Fetch
GET `/conversations/{conversation_id}/messages`  
Returns ordered messages with author_type to render chat history.

### Insights Fetch (consent-enforced)
GET `/insights?viewer_id=<uuid>`  
Only partner-shareable insights returned; raw partner messages are never exposed.

### Consent Grant/Revoke
POST `/consents/grant` or `/consents/revoke`
```json
{
  "user_id": "<uuid>",
  "scope": "summary.share",
  "target_partner_id": "<partner-uuid>"
}
```
Use granular scopes (e.g., `summary.share`, `resource.share`). List active consents via GET `/consents?user_id=...`.

### Screening Submission
POST `/screenings`
```json
{
  "user_id": "<uuid>",
  "instrument": "phq-2-lite",
  "answers": {"q1": 1, "q2": 2}
}
```
Returns trend status and flags. Frontend should show non-clinical language and optional escalation prompts.

### Escalation Prep
POST `/escalations/prepare`
```json
{
  "participants": ["<user-uuid>", "<partner-uuid>"],
  "allowed_context_ids": ["<summary-uuid>"]
}
```
Returns session ID; fetch context via GET `/escalations/{session_id}`. Only summaries/insights in `allowed_context_ids` may be shown.
