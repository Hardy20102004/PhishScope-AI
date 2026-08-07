# Enterprise Cloud Detection & Response (CDR) Platform - Architecture Guide

## Overview
Phase X-065 introduces the Cloud Detection & Response (CDR) platform, acting as the centralized nervous system for all cloud-native security telemetry within PHOENIX X. It ingests massive volumes of logs from AWS, Azure, GCP, and Kubernetes, normalizes them, and correlates isolated detections into unified investigations using an Entity-Graph approach.

## Architecture Components

### 1. Telemetry Normalization Engine (`telemetry_normalization_engine.py`)
Ingests disparate log formats (e.g., AWS CloudTrail, Azure Activity Logs, GKE Audit Logs) and normalizes them into a standard `CloudTelemetryEvent` schema. This abstracts away provider-specific syntax, allowing detection engineers to write rules against generic concepts like "Identity" and "Resource."

### 2. Cloud Detection Engine (`cloud_detection_engine.py`)
Continuously evaluates the normalized telemetry stream against a library of detection rules mapped to the MITRE ATT&CK framework (e.g., flagging Console Logins without MFA or unexpected privileged container executions).

### 3. Cloud Correlation Engine (`cloud_correlation_engine.py`)
Rather than relying solely on time-windows, this engine uses **Entity-Graph Correlation**. It links disparate detections across different platforms (e.g., an AWS IAM anomaly and an EKS runtime anomaly) if they share the same underlying entity (like `svc_legacy_deploy`). These are grouped into a `CloudInvestigation` container.

### 4. Response Coordination Engine (`response_coordination_engine.py`)
Analyzes active investigations and proposes human-approved containment playbooks (e.g., generating an action to `REVOKE_IAM_SESSIONS`). All actions remain in a `PENDING_APPROVAL` state until authorized by a SOC analyst.

### 5. CDR Risk Engine (`cdr_risk_engine.py`)
Calculates the dynamic priority of an investigation based on the criticality of the targeted resources and the severity of the grouped detections.

## Frontend Modules
- **CloudDetectionDashboard**: A high-level view showing ingestion metrics, live detection streams, and priority active investigations.
- **InvestigationWorkspace**: A detailed analyst interface that presents the AI-correlated attack narrative, combining timeline events and entity graphs into a cohesive story.
- **ResponseCoordinator**: The interface where SOC analysts review, modify, and approve AI-proposed containment actions.
- **CloudTimelineExplorer**: A granular, multi-cloud chronological search interface for raw, normalized telemetry.
