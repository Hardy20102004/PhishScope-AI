# Enterprise Cloud Workload Protection Platform (CWPP) - Architecture Guide

## Overview
Phase X-062 introduces the Enterprise CWPP to PHOENIX X. While CSPM (Phase X-061) focuses on static control plane configurations, CWPP focuses on the dynamic *runtime* layer. It continuously discovers active compute workloads (VMs, Pods, Serverless) and monitors OS-level events (processes, network, files) to detect behavioral anomalies and zero-day exploits.

## Architecture Components

### 1. Workload Discovery Engine (`workload_discovery_engine.py`)
Maintains an active inventory of compute instances. It abstracts the underlying compute architecture (whether it's an Azure VM or an AWS EKS Pod) into a generalized `CloudWorkload` object.

### 2. Runtime Visibility Engine (`runtime_visibility_engine.py`)
Acts as the high-throughput ingestion layer for telemetry streams coming from workload agents (e.g., eBPF sensors). It normalizes OS activities into standard `RuntimeEvent` records.

### 3. Behavior Analytics Engine (`behavior_analytics_engine.py`)
The AI brain of the CWPP. It evaluates incoming `RuntimeEvent` streams against established behavioral baselines. When a deviation occurs (e.g., a web server suddenly spawns a shell and opens an outbound connection), it generates a `BehaviorAnomaly` alert.

### 4. Workload Risk Engine (`workload_risk_engine.py`)
Aggregates active anomalies and maps them against the business criticality of the workload to produce a dynamic `WorkloadRiskScore`.

## Frontend Modules
- **WorkloadDashboard**: The primary command center showing the distribution of active compute resources and a live feed of behavioral anomalies.
- **RuntimeEventViewer**: A real-time, terminal-like stream of raw OS events for deep-dive investigations.
- **BehaviorAnalyticsDashboard**: A visual interface mapping specific anomalies (like an RCE) to MITRE ATT&CK tactics, providing explainable context to the security analyst.
- **WorkloadExplorer**: A searchable tabular inventory of all active and historical workloads.
