# Organization Onboarding Playbook

This playbook outlines the exact steps our Customer Success Managers (CSMs) follow when provisioning a new enterprise tenant.

## Phase 1: Provisioning (Day 1)
1. **Tenant Creation**: Run the `create_tenant.py` script via the internal VPN to provision the `Organization` in the database.
2. **Initial Admin**: Send a secure signup link to the designated IT Administrator for the client.
3. **SSO Configuration**: Schedule a 30-minute sync to configure SAML/OIDC metadata with the client's Identity Provider (Okta/Azure).

## Phase 2: Configuration & Integration (Week 1)
1. **Threat Feeds**: Have the client input their commercial API keys for VirusTotal, URLScan, etc., in the Admin portal.
2. **Custom Branding**: Upload the organization's logo and configure white-labeling domains if part of their tier.

## Phase 3: Rollout & Training (Week 2)
1. **Browser Extension Deployment**: Provide the client with the GPO/MDM deployment scripts to silently push the PHOENIX browser extension to their analysts' Chrome browsers.
2. **Investigator Training**: Conduct a 1-hour live walkthrough of the AI Copilot and Unified Investigation Engine using dummy phishing payloads.

## Phase 4: Health Check (Day 30)
Review adoption metrics via the internal analytics dashboard:
- Active Analysts (Weekly).
- AI Copilot prompts utilized.
- Mean Time to Investigate (MTTI) delta compared to pre-deployment baseline.
