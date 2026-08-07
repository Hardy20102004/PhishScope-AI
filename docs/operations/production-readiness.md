# Production Readiness Checklist

Before deploying PHOENIX to a production environment, ensure all items in this checklist are verified.

## 1. Security & Compliance
- [ ] Penetration Testing completed and Critical/High vulnerabilities remediated.
- [ ] Threat Model reviewed and signed off by Security Architecture.
- [ ] Secrets (Database passwords, API Keys) rotated and stored in AWS Secrets Manager / HashiCorp Vault.
- [ ] Network Policies applied in Kubernetes (Default Deny).
- [ ] TLS Certificates issued via Let's Encrypt / ACM and verified valid.

## 2. Infrastructure & Operations
- [ ] Database backups configured with Point-In-Time-Recovery (PITR) enabled.
- [ ] Disaster Recovery runbook tested (simulated failover).
- [ ] Kubernetes Horizontal Pod Autoscaler (HPA) configured and tested under load.
- [ ] Resource limits and requests defined for all containers to prevent noisy-neighbor issues.

## 3. Observability
- [ ] Telemetry logs successfully shipping to central SIEM (e.g., Datadog / ELK).
- [ ] Alerting rules configured for High Error Rates (5xx > 1%), DB CPU > 80%, and API Latency (p95 > 500ms).
- [ ] Incident Management dashboards verified operational.

## 4. Application
- [ ] Security regression test suite passed (`pytest backend/tests/security`).
- [ ] CORS strictly locked down to production domains (no `*`).
- [ ] Content Security Policy (CSP) headers verified in browser.
