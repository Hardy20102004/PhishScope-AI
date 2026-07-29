# Enterprise Cloud Identity & Entitlement Management (CIEM) Platform - Architecture Guide

## Overview
Phase X-064 introduces dedicated Identity Security and Entitlement Governance to PHOENIX X. The platform continuously discovers identities across multiple cloud environments (AWS, Azure, GCP), evaluates their complex entitlement chains, and identifies significant risks such as over-privileged dormant accounts.

## Architecture Components

### 1. Identity Discovery Engine (`identity_discovery_engine.py`)
Connects to Cloud Identity Providers (IdPs) and Cloud IAM services to inventory all Principals (Users, Groups, Roles, Service Accounts), tracking their metadata such as MFA status and last login date.

### 2. Entitlement Analysis Engine (`entitlement_analysis_engine.py`)
Parses deeply nested cloud IAM structures (Policies, Groups, Roles, SCPs) and computes a flattened "Effective Permissions" matrix for each identity. This simplifies "Who can do What" down to a normalized dataset.

### 3. Least Privilege Engine (`least_privilege_engine.py`)
Analyzes the effective permissions against actual usage telemetry. It identifies over-privileged accounts, unused entitlements, and critical hygiene issues like dormant administrators.

### 4. Identity Risk Engine (`identity_risk_engine.py`)
Aggregates the findings from the Least Privilege Engine to generate a holistic `IdentityRiskScore`.

### 5. Access Review Engine (`access_review_engine.py`)
Drives the Zero Trust governance workflow by generating periodic certification campaigns, requiring business owners to attest to or revoke access.

## Frontend Modules
- **IdentityDashboard**: A high-level, multi-cloud view of the organization's identity posture and largest risk areas.
- **PermissionExplorer**: An interactive matrix allowing security teams to search the flattened effective permissions across the entire cloud estate.
- **LeastPrivilegeDashboard**: Highlights specific identities that violate the principle of least privilege, providing immediate remediation actions (like generating a right-sized IAM policy).
- **GovernanceDashboard**: The workflow interface for managers and security teams to conduct periodic Access Reviews.
