# Enterprise Cloud Security Governance Platform - Architecture Guide

## Overview
Phase X-068 introduces the orchestration and governance layer of PHOENIX X. While the AI engines generate brilliant remediation recommendations, the platform adheres to a strict "Human-in-the-Loop" philosophy. No environment-changing actions can occur without explicit human approval.

## Architecture Components

### 1. Policy Management Engine (`policy_management_engine.py`)
Maintains the central repository of `SecurityPolicy` definitions. This is the source of truth for evaluating compliance across all clouds.

### 2. Workflow Engine (`workflow_engine.py`)
Manages the state transitions of `GovernanceWorkflow` records. Workflows move from `PLANNING` to `PENDING_APPROVAL`, to `APPROVED_FOR_EXECUTION`, and finally `COMPLETED`.

### 3. Approval Engine (`approval_engine.py`)
Enforces the **Hierarchical Approval Workflow**. For critical workflows (like modifying production IAM roles or altering Network Policies), the engine requires a signature chain, often culminating with the CISO. 

### 4. Automation Orchestration Engine (`automation_orchestration_engine.py`)
This engine actually makes the API calls out to AWS/Azure/GCP to enact change.
*Crucial Safety Mechanism*: The engine contains a hardcoded blocker (`if workflow.status != "APPROVED_FOR_EXECUTION": raise ValueError`) that prevents it from executing any destructive tasks without explicit clearance from the `ApprovalEngine`.

### 5. Compliance Monitoring Engine (`compliance_monitoring_engine.py`)
Continuously sweeps the unified asset inventory and compares it against active policies, updating the executive dashboards.

## Frontend Modules
- **PolicyDashboard**: Interface to build and version policies.
- **ApprovalDashboard**: The critical interface for SOC leads and CISOs to review context, evaluate risk, and digitally sign off on automated remediations.
- **WorkflowDashboard**: Real-time view of active orchestrations.
- **GovernanceDashboard**: Executive summary of compliance and throughput metrics.
