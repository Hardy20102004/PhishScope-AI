# Enterprise SOAR Playbook & Automation Platform - Architecture Guide

## Overview
The SOAR Platform (Phase X-036) enables analysts to design visual workflows, automate repetitive tasks, and enforce strict human-in-the-loop approval gates before executing security-sensitive containment actions.

## Architecture Components

### 1. Playbook Manager (`playbook_manager.py`)
Manages the CRUD operations and versioning of visual playbooks. A playbook consists of nodes (triggers, actions, flow control) and edges (execution paths) stored as a JSON blob.

### 2. Execution Engine (`execution_engine.py`)
A state machine that interprets the playbook schema. It traverses the graph, dispatching API requests to the `ConnectorManager` for automated tasks. If it encounters an `Approval Gate` node, the engine halts the execution state, sets it to `PAUSED_FOR_APPROVAL`, and awaits human intervention.

### 3. Approval Engine (`approval_engine.py`)
Manages the human-in-the-loop workflow. When an analyst reviews a pending approval via the UI, this engine validates their RBAC permissions and logs the decision. If approved, it signals the `ExecutionEngine` to resume traverse.

### 4. Connector Manager (`connector_manager.py`)
The unified interface layer for interacting with external enterprise systems (EDR, SIEM, Firewalls, Ticketing). Currently implemented with a mock layer simulating network latency and standardized response payloads.

### 5. AI Workflow Assistant (`ai_workflow_assistant.py`)
An intelligence layer that analyzes playbook topologies to suggest missing steps or improvements (e.g., suggesting a notification step after an isolation event).

## Database Schema Highlights
- **`Playbook`**: The workflow template.
- **`ExecutionHistory`**: A specific instance run of a playbook, tracking the active step and generating a detailed `execution_log`.
- **`ApprovalRecord`**: The audit trail for human decisions bound to an execution.

## Frontend Modules
- **SOARDashboard**: High-level telemetry on automation savings and playbook success rates.
- **WorkflowDesigner**: A visual, drag-and-drop canvas for designing playbooks.
- **ExecutionMonitor**: A live, auto-updating view tracing the path of a running playbook.
- **ApprovalCenter**: A centralized queue for Tier 2/3 analysts to review and authorize pending containment actions.
