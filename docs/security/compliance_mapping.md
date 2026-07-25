# Compliance Mapping & Privacy Assessment

This document maps PHOENIX's architectural controls to enterprise compliance standards.

## 1. Privacy Assessment (GDPR / CCPA)
- **Data Minimization**: The platform only stores evidence necessary for investigations.
- **Retention Policies**: Configurable per-tenant in `TenantSettings`. Soft-delete implemented via `is_active` flags before hard purging after 30 days.
- **Right to be Forgotten**: Global Admins can trigger complete tenant teardowns which cascade deletes across the database.

## 2. SOC 2 Trust Services Criteria Mapping
| Criteria | PHOENIX Control | Validation |
|----------|-----------------|------------|
| CC6.1 (Logical Access) | JWT Authentication, MFA via TOTP | `backend/app/core/security.py` |
| CC6.2 (RBAC) | Role-based endpoints (`Superuser`, `Admin`, `User`) | `backend/app/api/deps.py` |
| CC7.1 (System Monitoring) | Telemetry Middleware, Observability Dashboards | `backend/app/core/telemetry.py` |
| CC7.2 (Incident Response) | Incident Manager Dashboard for SREs | `frontend/.../IncidentManager.tsx` |
| CC8.1 (Change Management) | CI/CD GitHub Actions requiring PR approvals | `.github/workflows/cd.yml` |

## 3. OWASP ASVS (Application Security Verification Standard)
- **V2.1 Password Security**: Enforced bcrypt hashing for local credentials.
- **V3.1 Session Management**: JWT tokens issued with `exp` claims and signature verification.
- **V4.1 Access Control**: Implicit multi-tenant isolation utilizing `organization_id` filters in ORM queries.
- **V5.1 Input Validation**: Complete reliance on Pydantic schemas for Type coercion and boundary checking.
