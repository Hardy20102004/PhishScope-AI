# PhishScope-AI 2.0 (PHOENIX-X) — Official Presentation & Demo Guide
====================================================================
**Target Audience**: UP Police Cyber Cell, Senior Police Officials & Forensic Evaluators  
**Developed by**: Umesh Gupta (National Forensic Sciences University, Tripura Campus)  
**Platform Version**: 2.0.0-gemini  

---

## 1. Executive Summary

**PhishScope-AI** is an advanced, AI-powered Digital Forensics, Incident Response (DFIR), and Phishing Investigation Platform specifically architected for Indian Law Enforcement & Cyber Cell Investigating Officers (IOs).

### Key Value Propositions
* 🤖 **AI-Driven Threat Narratives**: Integrates **Google Gemini 3.6-flash / 3.5-flash** to transform complex technical indicators (IOCs) into plain-English and **Hindi case summaries**.
* 🇮🇳 **Indian Banking & UPI Fraud Engine**: Deep pattern recognition for Indian financial scams (SBI, HDFC, ICICI, Paytm, PhonePe, GooglePay VPA handle impersonation, fake APK droppers).
* 📊 **Enterprise Cyber Fusion**: 95+ forensic and security modules covering Mobile, Disk, Memory, Cloud (CSPM/CWPP/CIEM/CDR), AppSec (SAST/DAST/SCA), Zero Trust (ZTA), and MITRE ATT&CK Attack Graphs.
* 🌐 **Real-Time Extension Protection**: Includes a Chrome Extension (Manifest v3) for instantaneous browser threat prevention and active URL inspection.

---

## 2. 5-Minute Presentation Script for Officials

### ⏱️ Minute 1: The Problem — The Escalating Cyber Scam Landscape in India
> *"Good morning/afternoon respected officials. Cyber crime in India has evolved rapidly. Citizens are daily targeted with fake APK links, UPI QR code payment scams, and deceptive banking sites impersonating SBI, Paytm, or IRCTC. Investigating Officers face hundreds of reported URLs and suspicious devices daily, taking hours or days to manually analyze each incident."*

### ⏱️ Minute 2: The Solution — PhishScope-AI 2.0
> *"PhishScope-AI is built specifically to automate and accelerate this entire investigation lifecycle. By pairing deep forensic engines with Google Gemini AI, PhishScope-AI analyzes malicious URLs, QR codes, email headers, mobile artifacts, and network traffic in seconds—delivering actionable threat intelligence immediately."*

### ⏱️ Minute 3: Live Demonstration — Real-Time Analysis & Hindi Report Export
> *(Perform Live Demo Sample 1 & Sample 3 below)*
> *"Let me show you a real-world example. Here we input a reported fake SBI netbanking link. PhishScope-AI immediately extracts domain age, SSL certificate details, brand spoofing scores, and IOCs. With a single click, it generates a comprehensive **Hindi Summary Report** ready for inclusion in police case diaries or FIR filings."*

### ⏱️ Minute 4: Comprehensive DFIR & Cloud Security Scope
> *"Beyond phishing, PhishScope-AI serves as a full-spectrum SOC and Digital Forensics suite. It includes 95+ enterprise modules—from mobile SMS & call log timeline analysis to memory forensics, MITRE ATT&CK visual graphs, and real-time browser protection via our Chrome Extension."*

### ⏱️ Minute 5: Conclusion & Operational Impact
> *"In summary, PhishScope-AI drastically reduces investigation time from days to seconds, empowers non-technical Investigating Officers with AI-generated Hindi insights, and equips senior officials with executive threat dashboards. Thank you, and I am open to your questions."*

---

## 3. Step-by-Step Live Demo Runbook

### Pre-Demo Checklist
1. Launch the platform:
   ```bash
   chmod +x start_mac.sh && ./start_mac.sh
   # OR: python run_phishscope.py
   ```
2. Open Browser: `http://localhost:3000`
3. Credentials:
   - **Email**: `admin@phoenix.ai`
   - **Password**: `Phoenix@Admin123`

---

### Demo Scenario 1: Fake Banking URL & AI Narrative
1. Navigate to **URL Intelligence** from the left navigation bar.
2. Enter sample URL: `http://sbi-kyc-update-online.com/login`
3. Click **Analyze URL**.
4. Highlight to officials:
   - Risk Score & Severity Badge (`CRITICAL / HIGH`)
   - Domain creation age & SSL validation check
   - Gemini AI Automated Narrative explaining the attack vector
   - Detected Brand Impersonation: **State Bank of India (SBI)**

---

### Demo Scenario 2: UPI Fraud & QR Code Analysis
1. Navigate to **QR Intelligence / Mobile Forensics**.
2. Upload/Paste a suspicious UPI payment link or QR code payload (e.g., `upi://pay?pa=scammer@paytm&pn=ElectricityBoard&am=5000`).
3. Click **Deconstruct Payload**.
4. Highlight to officials:
   - Identification of mismatched VPA handle (`ElectricityBoard` vs suspicious VPA `scammer@paytm`)
   - Automated UPI Scam Risk Rating.

---

### Demo Scenario 3: Hindi Intelligence Report Export
1. On any completed analysis page, click **Export Report**.
2. Toggle Language to **Hindi (हिंदी)**.
3. Show the generated formal threat summary in Hindi for UP Police IO case diary documentation.

---

### Demo Scenario 4: Chrome Extension Active Protection
1. Open Chrome Extension menu.
2. Show active URL monitoring & real-time phishing block notification interface.

---

## 4. Frequently Asked Questions (Q&A) Guide

### Q1: How does PhishScope-AI detect Indian-specific banking and UPI scams?
**Answer**: PhishScope-AI maintains specific heuristic models and regex patterns for Indian banking infrastructure (SBI, HDFC, ICICI, Axis, PNB, IRCTC) and UPI VPA verification algorithms (Paytm, PhonePe, GooglePay, BHIM) to catch brand impersonation and payment request manipulation.

### Q2: What if internet connectivity or the AI API is offline during a field investigation?
**Answer**: PhishScope-AI features an automatic offline fallback mode. If external AI services are unreachable, local rule-based forensic engines, SQLite databases, and heuristic analyzers handle the investigation smoothly.

### Q3: Is citizen and investigation data kept secure and confidential?
**Answer**: Yes. All telemetry and case reports are encrypted using AES-256 at rest and TLS 1.3 in transit. Role-based access control (RBAC) ensures only authorized law enforcement personnel can view case data.

### Q4: Can non-technical police officers use this platform effectively?
**Answer**: Absolutely. The core design philosophy of PhishScope-AI is accessibility. The Gemini AI engine translates complex technical IOCs into natural language and localized Hindi summaries, allowing IOs at any technical level to understand and act on the findings.

---
*PhishScope-AI 2.0 — Prepared for UP Police Cyber Cell Official Evaluation.*
