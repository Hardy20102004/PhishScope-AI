# Support Incident Escalation Playbook

## Tier 1 Support (Help Desk)
- **Scope**: Password resets, UI navigation questions, browser extension installation errors.
- **SLA**: Initial response within 4 hours.
- **Action**: Resolve using knowledge base articles. If the issue involves a backend error or missing data, escalate to Tier 2.

## Tier 2 Support (Application Support)
- **Scope**: API integration failures, Threat Feed connector errors, SSO/SAML configuration debugging.
- **SLA**: Initial response within 1 hour.
- **Action**: Review application logs via the internal Datadog dashboard. Instruct the customer on how to correct integration payloads. If there is a suspected bug in the core platform, escalate to Tier 3 via Jira.

## Tier 3 Support (Engineering / SRE)
- **Scope**: Platform outages, data corruption, critical security vulnerabilities.
- **SLA**: Initial response within 15 minutes (24/7 PagerDuty).
- **Action**: Follow the engineering `incident_response.md` runbooks to mitigate platform-wide faults. Update the public status page (`status.phoenix-platform.com`) immediately.
