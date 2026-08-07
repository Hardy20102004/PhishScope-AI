# Incident Response Plan

## 1. Preparation
- **Monitoring**: All SREs must have access to the Observability Dashboards (`/admin/observability`).
- **Escalation**: PagerDuty integration handles critical paging for infrastructure faults.

## 2. Identification
If an alert is triggered (e.g., via PagerDuty or the Incident Manager dashboard), determine the scope:
- **Severity 1 (Critical)**: Total platform outage or confirmed data breach.
- **Severity 2 (High)**: Major feature degradation (e.g., AI Copilot offline).
- **Severity 3 (Medium)**: Localized issue (e.g., Single Threat Feed connector failing).

## 3. Containment
### Data Breach / Account Takeover
1. Immediately lock the compromised user account via the `Admin -> User Management` dashboard.
2. Force an MFA reset.
3. Review `AuditLogs` to determine the blast radius of accessed files.

### Volumetric Attack (DDoS)
1. Verify WAF (Web Application Firewall) rules.
2. Ensure NGINX ingress rate limiting is aggressively dropping packets.
3. Scale backend pods via HPA if valid traffic is being starved.

## 4. Eradication & Recovery
1. Deploy hotfix or rollback to a known good state via Kubernetes Deployment revisions.
2. If database corruption occurred, initiate PITR (Point in Time Recovery) via AWS RDS console.
3. Close the Incident in the SRE Dashboard with resolution notes.

## 5. Post-Incident
- Conduct a blameless post-mortem within 48 hours.
- Update this runbook with new findings.
