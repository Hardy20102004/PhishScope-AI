# Enterprise Detection Rule Engine - Architecture Guide

## Overview
The Enterprise Detection Rule Engine (Phase X-032) is the centralized platform for creating, validating, testing, and managing detection content (Sigma, YARA, Custom) within PHOENIX X. It strictly separates rule authoring and testing from deployment to ensure all detections are robust, explainable, and explicitly approved.

## Architecture Components

### 1. Database Schema (`models/detection.py`)
- **DetectionRule**: The parent entity representing a unique detection concept. Tracks current status, ownership, and MITRE mapping.
- **DetectionRuleVersion**: Immutable records of the rule payload at a specific point in time, enabling rollbacks and complete historical tracking.
- **RuleTestResult**: Records the results of regression testing against a specific rule version.
- **RuleApprovalRecord**: The audit trail for state transitions.

### 2. Rule Validation Engine (`validation.py`)
Validates rule payloads synchronously during the authoring phase. It enforces YAML schema checks for Sigma and structural checks for YARA to prevent broken rules from entering the `DRAFT` state.

### 3. Rule Testing Engine (`testing.py`)
A simulation engine that runs rules against benchmark datasets (e.g., historical alerts, synthetic payloads) to calculate Coverage, False Positives (FP), and False Negatives (FN).

### 4. Approval Workflow Engine (`workflow.py`)
A strict state machine managing the rule lifecycle:
`DRAFT` -> `IN_REVIEW` -> `APPROVED` -> `READY_FOR_DEPLOYMENT` -> `DEPLOYED` -> `RETIRED`.
**Critical Control**: The engine programmatically blocks transitions to `APPROVED` if the `RuleTestResult` indicates failing regression tests.

### 5. Rule Authoring Engine (`authoring.py`)
Provides the core logic for the Rule Editor and integrates with the `AI Context Engine` to generate MITRE ATT&CK mapping suggestions and human-readable explanations of the code.

## Frontend Dashboard
The React frontend provides four main views:
- **DetectionDashboard**: Operational metrics and workflow activity.
- **RuleExplorer**: Central registry of all detection content.
- **RuleEditor**: A dual-pane IDE featuring syntax highlighting, live validation, and an AI Assistant side-panel.
- **TestingDashboard**: Visualization of regression test results and coverage metrics.
