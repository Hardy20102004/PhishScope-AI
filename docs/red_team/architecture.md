# Enterprise Red Team Campaign Platform - Architecture Guide

## Overview
The Red Team Campaign Management Platform (Phase X-052) handles the governance, scoping, authorization, and tracking of authorized adversarial simulations. It enforces strict legal and operational gates to ensure that high-risk testing is conducted safely and transparently.

## Architecture Components

### 1. Campaign Manager (`campaign_manager.py`)
Orchestrates the lifecycle of a `RedTeamCampaign`. Enforces a strict state machine: `DRAFT` -> `PENDING_APPROVAL` -> `AUTHORIZED` -> `IN_PROGRESS` -> `COMPLETED`. 

### 2. Authorization Manager (`authorization_manager.py`)
Provides the cryptographic governance layer. Before a campaign can move to `IN_PROGRESS`, all assigned stakeholders (e.g., CISO, Legal Counsel, System Owners) must digitally sign an `AuthorizationRecord`. The engine generates a SHA-256 hash incorporating the campaign scope and timestamp to simulate a non-repudiable signature.

### 3. Findings Manager (`findings_manager.py`)
Tracks the output of a campaign. When the Red Team identifies a vulnerability or a detection gap, it is logged as a `CampaignFinding` and mapped to specific MITRE ATT&CK techniques, allowing the organization to track remediation efforts post-campaign.

## Frontend Modules
- **CampaignPlanner**: Interface for defining the Rules of Engagement (RoE) and strictly separating in-scope vs. out-of-scope assets.
- **ApprovalCenter**: A dedicated portal for executives and legal counsel to review campaign scopes and apply their digital signatures.
- **FindingsDashboard**: A tracking matrix for identified gaps, ensuring that Red Team insights translate directly into defensive improvements.
