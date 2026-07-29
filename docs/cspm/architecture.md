# Enterprise Cloud Security Posture Management (CSPM) Platform - Architecture Guide

## Overview
Phase X-061 introduces the Enterprise CSPM Platform to PHOENIX X. This module is responsible for continuous multi-cloud asset discovery, configuration assessment, and compliance monitoring across AWS, Azure, and GCP. It identifies misconfigurations (e.g., exposed storage, overly permissive IAM) and provides AI-driven remediation guidance.

## Architecture Components

### 1. Cloud Asset Discovery Engine (`asset_discovery_engine.py`)
Provides a generalized, provider-agnostic ingestion layer for multi-cloud assets. It normalizes distinct resource types (like AWS EC2 and Azure VMs) into standard `CloudAsset` objects, allowing cross-cloud visibility.

### 2. Risk Assessment Engine (`risk_assessment_engine.py`)
Evaluates the raw JSON configurations of discovered assets to identify specific security risks. It assigns severity scores based on the combination of factors (e.g., a resource being both public and unencrypted yields a CRITICAL severity `CloudMisconfiguration`).

### 3. Compliance Engine (`compliance_engine.py`)
Maps identified asset states back to major industry benchmarks (CIS Foundations, NIST CSF, SOC 2, ISO 27001). It generates `ComplianceFinding` records that aggregate pass/fail metrics at the control level.

## Frontend Modules
- **CloudSecurityDashboard**: The apex view summarizing the multi-cloud posture, top critical misconfigurations by service, and high-level CIS compliance.
- **CloudAssetExplorer**: A unified, searchable inventory of all normalized cloud resources across all connected providers.
- **MisconfigurationViewer**: A detailed investigation view for specific risks. Crucially, it displays the exact failing JSON configuration block and provides AI-generated CLI commands to auto-remediate the issue.
- **ComplianceDashboard**: A visual representation of enterprise alignment with standard frameworks, showing clear pass/fail ratios per benchmark.
