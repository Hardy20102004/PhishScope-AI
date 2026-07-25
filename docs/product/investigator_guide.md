# Investigator Guide

Welcome to PHOENIX. This guide will walk you through the core workflows for analyzing digital threats.

## 1. Starting an Investigation
From the **Dashboard**, click the primary **New Investigation** button.
1. Select the artifact type: URL, Email (EML/MSG file), Image, or Text.
2. Provide the artifact or upload the file.
3. Click **Analyze**.
The Unified Investigation Engine will parse the artifact, extract IOCs (IPs, Domains, Hashes), and query configured Threat Feeds.

## 2. Using the AI Copilot
The AI Copilot is context-aware and understands the investigation you are currently viewing.
- Click the **Copilot** tab on the right side of the Investigation screen.
- Ask questions like:
  - *"Summarize the intent of this phishing email."*
  - *"Are there any obfuscated JavaScript payloads in this HTML?"*
  - *"Draft an executive summary for this case."*

## 3. Case Management
You can group multiple related investigations into a single **Case**.
1. Navigate to the **Cases** view via the sidebar.
2. Create a new Case (e.g., "Q3 Spear-Phishing Campaign").
3. Link existing investigations to this Case.
4. Add markdown-formatted notes and collaborate with your team.

## 4. Exporting Evidence
Once an investigation is concluded, you can generate a forensically sound PDF report.
- Click the **Export Report** button in the top right of the Investigation view.
- The exported PDF includes a cryptographic hash of the original evidence to maintain the Chain of Custody.
