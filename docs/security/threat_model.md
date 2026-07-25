# PHOENIX Threat Model

This document outlines the threat landscape for the PHOENIX platform using the STRIDE methodology.

## 1. Trust Boundaries
- **Internet Boundary**: Between public internet and the NGINX Ingress controller.
- **API Boundary**: Between the React Frontend / Browser Extension and the FastAPI backend.
- **Tenant Boundary**: Between the isolated data segments of distinct enterprise organizations.
- **External API Boundary**: Between PHOENIX backend and 3rd-party Threat Feeds (VirusTotal, URLScan).

## 2. STRIDE Analysis

### Spoofing (Authentication)
**Threat**: An attacker attempts to impersonate a legitimate investigator or administrator.
**Mitigation**: 
- Enforce strict JWT-based authentication with short expiration windows.
- OAuth2.0 / SAML integration for Enterprise Tenants.
- Mandatory Multi-Factor Authentication (MFA) via TOTP.

### Tampering (Integrity)
**Threat**: A malicious user modifies evidence metadata or audit logs.
**Mitigation**:
- Immutable Audit Logs via database constraints.
- Chain of Custody hashes (SHA-256) calculated at the time of evidence acquisition.
- Write-once-read-many (WORM) storage configurations for exported reports.

### Repudiation (Non-repudiation)
**Threat**: A user denies taking an action (e.g., deleting a case or exporting data).
**Mitigation**:
- Comprehensive Audit Log table capturing `user_id`, `action`, `resource`, `timestamp`, and `ip_address`.
- Audit logs are read-only and visible to Global Administrators.

### Information Disclosure (Confidentiality)
**Threat**: Broken Object Level Authorization (BOLA) leads to cross-tenant data leakage.
**Mitigation**:
- SQLAlchemy ORM base scopes all queries implicitly using the current user's `organization_id`.
- Strict Transport Security (HSTS) and AES-256 Encryption at Rest.

### Denial of Service (Availability)
**Threat**: Volumetric attacks or computationally expensive AI prompts exhaust system resources.
**Mitigation**:
- Rate limiting at the NGINX Ingress layer and FastAPI middleware.
- Timeout limits on LLM generation endpoints.
- Auto-scaling EKS pods based on CPU/Memory thresholds.

### Elevation of Privilege (Authorization)
**Threat**: A standard investigator attempts to modify tenant-wide security policies.
**Mitigation**:
- Strict Role-Based Access Control (RBAC) enforced via FastAPI `Security` dependencies (e.g., `Depends(get_current_active_superuser)`).
