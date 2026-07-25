# API & Operations Guide

## REST API Endpoints

The Multi-Agent framework exposes the following core endpoints (`/api/v1/multi-agent`):

### `GET /agents`
Returns the active workforce roster, including agent IDs, capabilities, health status, and load metrics.

### `POST /plan`
Accepts a raw text objective and returns the generated Execution DAG (Directed Acyclic Graph) of agent tasks.

### `POST /execute/{plan_id}`
Fires the asynchronous DAG Execution Engine in a background task.

### `GET /approvals`
Lists all pending Human-in-the-Loop authorization requests.

### `POST /approvals/{request_id}/decision`
Submits an analyst decision (APPROVE, REJECT, OVERRIDE) to resume a paused agent workflow.

### `GET /stream/{plan_id}`
An SSE (Server-Sent Events) endpoint that streams live `CommunicationBus` messages to the frontend UI for real-time observability.

## Observability & Health

The `AgentHealthMonitor` tracks:
*   **Latency**: Execution time per agent.
*   **Error Rates**: Timeout frequency and orchestration failures.
*   **Utilization**: Number of tasks handled in a trailing 24-hour window.

The `AgentAuditService` provides immutable compliance logging for every action taken by an autonomous agent, ensuring complete traceability.
