# 🩺 SLACK INTELLIGENCE (GABRIEL SYSTEM)

## Authorization Scopes

**Source:** User Directive (2025-12-23)

### `authorizations:read` Scope

- **Purpose**: Grants permission to list authorizations associated with the Events API.
- **Requirement**: Must be used with an **App-Level Token**.
- **Usage**:
  - App-level tokens represent the app across an entire organization.
  - Obtain via **App Management > Basic Information > App-Level Tokens**.
  - Request the scope via **OAuth & Permissions** or update OAuth flow.

### Key API Methods

- `apps.event.authorizations.list`

### Implementation Note

This is critical for granular event visibility and ensuring the Slack bot ("Slack Worker") operates correctly within the workspace constraints.
