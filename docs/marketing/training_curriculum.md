# PHOENIX Training Curriculum

## 1. SOC Analyst Onboarding (2 Hours)
**Objective**: Enable Tier 1/2 analysts to quickly ingest, analyze, and close phishing tickets using PHOENIX.
- **Module 1: The Unified Dashboard**: Navigating the UI, understanding artifact types.
- **Module 2: Running an Investigation**: Uploading an `.eml` file, reviewing Extracted IOCs, and understanding Threat Feed scores.
- **Module 3: AI Copilot**: Best practices for prompting the LLM. Using the Copilot to draft a summary for a ServiceNow ticket.
- **Module 4: Case Management & Export**: Grouping artifacts into a Case and exporting the final PDF report.

## 2. Administrator Training (1 Hour)
**Objective**: Teach tenant administrators how to manage users, security policies, and integrations.
- **Module 1: User & Role Management**: Inviting users, configuring RBAC.
- **Module 2: SSO Configuration**: Setting up SAML 2.0 with Okta.
- **Module 3: Threat Feeds**: Provisioning API keys for VirusTotal and URLScan.

## 3. Hands-On Lab Scenarios
We provide a standard ZIP file of sanitized malware artifacts for training:
- **Scenario A**: A simulated CEO Fraud email (Business Email Compromise). Analysts must extract the reply-to address and identify the spoofing technique.
- **Scenario B**: A credential harvesting link sent via SMS. Analysts must use the URL Investigation engine to safely render the DOM and identify the exfiltration endpoint.
