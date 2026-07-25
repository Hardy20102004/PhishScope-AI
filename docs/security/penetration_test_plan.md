# Penetration Testing Plan

## 1. Scope
The scope of this engagement covers the PHOENIX AI Digital Scam Investigation Platform.

**In Scope:**
- `app.phoenix-platform.com` (React Frontend)
- `api.phoenix-platform.com` (FastAPI Backend)
- Browser Extension (Static Analysis & API Calls)
- External integrations (Threat Feeds) - **Simulated environments only**

**Out of Scope:**
- Load testing / DDoS attacks.
- Social Engineering / Phishing of internal staff.
- Physical Security.

## 2. Methodology (OWASP Top 10)
Assessors must execute test cases mapped against the OWASP Top 10 API and Web App vulnerabilities:
1. **Broken Object Level Authorization (BOLA)**: Attempt to read/modify cases across tenant boundaries.
2. **Broken Authentication**: Test password reset flows, JWT hijacking, and brute-force protections.
3. **Excessive Data Exposure**: Verify endpoints do not leak PII or evidence metadata in raw JSON.
4. **Lack of Resources & Rate Limiting**: Attempt to flood the AI Copilot endpoint to trigger rate limits.
5. **Security Misconfiguration**: Inspect HTTP response headers (CSP, HSTS).
6. **Injection**: Provide Malicious prompts (Prompt Injection) to the AI Copilot and XSS payloads in case notes.

## 3. Reporting
All vulnerabilities must be reported with:
1. CVSS v3.1 Score.
2. Steps to reproduce.
3. PoC (Proof of Concept).
4. Recommended remediation.
