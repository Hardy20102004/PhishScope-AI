# Administrator Guide

This guide is intended for Tenant Administrators (`Admin` Role) managing their organization's PHOENIX instance.

## 1. User & Role Management
Navigate to **Admin -> User Management** via the sidebar.
- **Invite Users**: Click "Invite User", specify their email, and assign a role.
- **Roles**:
  - `User`: Can create and view investigations.
  - `Analyst`: Can edit cases, execute workflows, and export reports.
  - `Admin`: Full control over the tenant, including billing and security policies.

## 2. API Key Generation
To integrate PHOENIX with your internal SIEM or SOAR platform, generate an API key.
- Navigate to **Admin -> API Keys**.
- Click "Generate New Key". 
- **Important**: Store this key securely. It is only displayed once and provides programmatic access to your tenant's data.

## 3. Threat Intel Configuration
PHOENIX supports bring-your-own-key (BYOK) for Threat Intelligence providers.
- Navigate to **Admin -> Integrations**.
- Input your organization's API keys for VirusTotal, URLScan, or AbuseIPDB.
- Once configured, the Unified Investigation Engine will automatically query these providers during URL/IP analysis.

## 4. Audit Logs
To review administrative or investigative actions:
- Navigate to **Admin -> Audit Logs**.
- You can filter by Date, User, or Action Type (e.g., `CASE_EXPORT`, `USER_DELETED`).
