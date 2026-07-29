# Enterprise Multi-Cloud Security Intelligence Platform - Architecture Guide

## Overview
Phase X-067 introduces the apex aggregation layer of PHOENIX X: the **Multi-Cloud Security Intelligence Platform**. This module does not perform raw data collection itself; instead, it ingests processed findings from CSPM, CWPP, CIEM, DSPM, and CDR, fusing them into a unified operational view.

## Architecture Components

### 1. Unified Asset Engine (`unified_asset_engine.py`)
Provides a single, normalized `UnifiedCloudAsset` schema that can represent an AWS EC2 instance (from CWPP), an Azure AD user (from CIEM), or a GCP BigQuery dataset (from DSPM).

### 2. Cross-Cloud Correlation Engine (`cross_cloud_correlation_engine.py`)
Builds relationships between these assets. This allows the system to trace a toxic combination across cloud boundaries (e.g., an over-privileged Azure AD identity assuming an AWS IAM role that has access to unencrypted PII).

### 3. Unified Risk Engine (`unified_risk_engine.py`)
Calculates the top-level **Enterprise Cloud Risk Score**.
**Strategy**: It uses a *Critical Path Strategy* rather than a weighted average. This ensures that exponential risk paths (like the toxic combination mentioned above) severely impact the global score, rather than being "watered down" by thousands of secure, low-risk assets.

### 4. Compliance Analytics Engine (`compliance_analytics_engine.py`)
Rolls up framework alignment (NIST, CIS, ISO) from the underlying cloud environments into an aggregated enterprise compliance percentage.

### 5. Executive Intelligence Engine (`executive_intelligence_engine.py`)
Distills complex graph analytics into human-readable executive summaries, highlighting strategic, multi-cloud improvements.

## Frontend Modules
- **UnifiedCloudDashboard**: The primary landing page for the CISO/Cloud Architect, showing the global risk score and multi-cloud breakdown.
- **CrossCloudRiskDashboard**: Operational view focusing on *Toxic Combinations* that cross domains (CSPM + CIEM + DSPM).
- **ComplianceDashboard**: Aggregated auditor view for NIST/CIS alignment.
- **MultiCloudAssetExplorer**: A unified search interface to find any asset across any cloud environment.
