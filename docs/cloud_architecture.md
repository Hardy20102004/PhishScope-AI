# Enterprise Threat Intelligence Cloud Architecture

## Overview
The Enterprise Threat Intelligence Cloud is a secure, multi-tenant environment designed for controlled intelligence sharing, cross-organization federation, and collaborative analysis. It serves as the backbone for sharing indicators, attack graphs, threat actor profiles, and campaign intelligence across regions and partners.

## Core Components

### 1. Tenant Manager
Provides logical isolation between organizations, departments, or managed clients.
- Multi-tier hierarchy (Parent/Child tenants).
- Strict data separation at the database layer (via `tenant_id`).

### 2. Workspace Manager
Allows teams to collaborate on specific tasks (e.g., SOC Incidents, Threat Hunting).
- RBAC support via `WorkspaceMember` (OWNER, EDITOR, VIEWER, CONTRIBUTOR).
- Multiple workspace types: Private, Shared, Incident, Campaign, Research, Read-Only, Collaboration.

### 3. Federation Engine & Synchronization
Enables Cross-Organization intelligence exchange via TAXII 2.1 / STIX 2.1.
- Synchronizes intelligence via Full Sync and Incremental Pulls/Pushes.
- Tracks sync history and handles connection configurations (mTLS, API Key, OAuth2) for external `FederationNode`s.

### 4. Sharing Policy Engine & Governance
Enforces data classification and approval workflows before intelligence is shared.
- Applies minimum TLP restrictions.
- Supports Anonymization of sources and specific target audience restrictions.
- Creates immutable logs via `AuditService` when intelligence leaves the tenant boundary.

### 5. Version Manager & Conflict Resolution
Ensures data integrity during concurrent updates across the federation.
- Automatically increments versions for Shared Intelligence Objects.
- Detects conflicts when remote and local versions diverge.
- Allows for conflict resolution strategies: Keep Local, Accept Remote, Manual Merge.

## Analytics
Built-in `AnalyticsEngine` aggregates statistics on sharing velocity, active collaborators, and federation node health, powering the frontend dashboards.
