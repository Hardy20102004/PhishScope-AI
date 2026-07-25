# Enterprise Cloud Investigation Platform Architecture

## Overview
The Cloud Investigation Platform (PHOENIX Phase X-020) provides structured forensic analysis of lawfully acquired cloud evidence (e.g., AWS CloudTrail logs, Azure AD exports, GCP Asset Inventories). It extracts assets, identities, configurations, and audit events to build a unified chronological timeline and leverages the AI Brain for threat correlation.

## Architecture Components

### Backend (`app/cloud_investigation/`)
1. **CloudArtifactParserEngine**: Simulates the parsing of raw cloud logs (JSON format) into structured dictionaries for Assets, Identities, Configurations, and Audit Logs.
2. **CloudAssetEngine**: Analyzes virtual machines, storage buckets, and functions to identify public exposure or misconfigurations.
3. **CloudIdentityEngine**: Analyzes users, roles, and permissions, identifying highly privileged or dormant accounts.
4. **ConfigurationAnalysisEngine**: Analyzes IAM policies and network security rules for risky configurations (e.g., overly permissive policies).
5. **AuditLogAnalysisEngine**: Analyzes login events, resource creation, and administrative actions for anomalous sequences (e.g., defense evasion).
6. **TimelineEngine**: Merges asset creation, identity changes, and audit events into a unified, chronologically sorted `CloudTimelineEvent` list.
7. **IOCExtractionEngine**: Extracts actionable cloud indicators (IPs, Actor IDs) from the audit logs.
8. **RiskAssessmentEngine**: Computes an overall risk score based on anomalous audit events, overly permissive identities, and public assets.
9. **CloudInvestigationManager**: Asynchronously orchestrates the extraction, timeline generation, and correlation pipeline.
10. **CloudAIIntegration**: Generates a human-readable threat narrative summarizing the forensic anomalies in the cloud capture.

### Frontend (`frontend/src/features/cloud-investigation/`)
- **CloudInvestigationDashboard**: The main control center for simulating forensic data uploads and viewing the results.
- **AssetExplorer**: Tabular view of cloud assets (VMs, Buckets).
- **IdentityExplorer**: Tabular view of cloud identities and their permissions.
- **ConfigurationViewer**: Viewer for security policies and misconfigurations.
- **AuditLogViewer**: Displays audit events (e.g., AWS CloudTrail logs), highlighting anomalies.
- **TimelineViewer**: A unified chronological feed of all parsed events, enabling analysts to trace timelines (e.g., login followed by defense evasion).
- **CloudAIFindings**: Renders the AI-generated forensic narrative.

## Data Models
Stored in `app/models/cloud_investigation.py`:
- `CloudInvestigation`: Central link to the PHOENIX investigation graph.
- `CloudAsset`: Infrastructure resources (EC2, S3, etc.).
- `CloudIdentity`: Users, Roles, Groups, and their permissions.
- `CloudConfiguration`: JSON configurations (IAM Policies).
- `CloudAuditEvent`: Log events indicating "Who did what, when, and from where."
- `CloudTimelineEvent`: Unified chronological data model.
- `ExtractedCloudIOC`: Extracted IPs and Cloud Identifiers.

## Future Roadmap & Vision
- **True Cloud API Integration**: Directly query AWS/Azure/GCP APIs (read-only) for live asset and identity ingestion.
- **Identity Graph Visualization**: Visual mapping of IAM roles, permissions, and privilege escalation paths (BloodHound for Cloud).
- **CSPM Integration**: Integrate Cloud Security Posture Management rules to systematically evaluate misconfigurations against CIS Benchmarks.
