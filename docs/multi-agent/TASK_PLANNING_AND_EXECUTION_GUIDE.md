# Task Planning & Execution Guide

PHOENIX X transitions from single-shot LLM requests to **Asynchronous DAG Execution**.

## 1. Intent Detection & Task Decomposition

When a user submits a broad query (e.g., "Investigate this suspicious email and tell me if the domain is safe"), the `TaskPlanner` intercepts the request.

It leverages the AI Security Brain to decompose the objective into granular tasks:
1.  **Task A**: Extract EML headers (Assigned to: `email-analysis-agent`)
2.  **Task B**: Extract URLs (Assigned to: `url-analysis-agent`)
3.  **Task C**: Correlate Domain Reputation (Assigned to: `threat-intel-agent`, **Depends on B**)
4.  **Task D**: Synthesize Final Report (Assigned to: `report-writer-agent`, **Depends on A, C**)

## 2. DAG Execution Engine

The `ExecutionEngine` operates on the generated plan:
*   It utilizes Python `asyncio` to execute independent tasks concurrently (e.g., Tasks A and B run in parallel).
*   It monitors task completion and forwards outputs to dependent tasks (e.g., Output of B is injected into the payload for C).
*   It handles transient failures via retry backoff logic.

## 3. Human-in-the-Loop (HITL) Gating

If an agent attempts a high-risk action (e.g., quarantine a host) or if the `ConflictResolver` detects contradictory agent findings with a composite confidence score `< 0.70`, the `HumanInTheLoopEngine` interrupts the DAG.

*   The engine pauses the `asyncio` execution path.
*   It emits an SSE `APPROVAL_REQUIRED` event over the `CommunicationBus`.
*   A human analyst uses the Frontend command center to `APPROVE`, `REJECT`, or `OVERRIDE`.
*   The DAG execution resumes automatically upon resolution.
