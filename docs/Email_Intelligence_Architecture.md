# Enterprise Email Intelligence Platform Architecture

## Overview
The Enterprise Email Intelligence Platform (PHOENIX Phase X-013) provides forensic-grade investigation capabilities for raw email files (RFC 5322 `.eml`). It automatically dissects an email into its constituent parts—headers, routing infrastructure, authentication signals, body linguistics, and attachments—to provide a comprehensive, AI-explained threat narrative.

## Architecture Components

### Backend (`app/email_intelligence/`)
1. **EmailParserEngine**: Utilizes the native Python `email` (modern API) to robustly parse raw EML structures, decoding MIME boundaries, extracting inline HTML/Text, and isolating binary attachments.
2. **HeaderAnalysisEngine**: Normalizes and extracts standard RFC headers (Message-ID, Date, Subject, From, To).
3. **AuthenticationAnalysisEngine**: Parses the `Authentication-Results` header to determine the validity of SPF, DKIM, and DMARC checks, flagging spoofing attempts.
4. **RoutingAnalysisEngine**: Reconstructs the mail delivery path by analyzing the `Received` header chain, identifying the true origin IP and upstream relays.
5. **ConversationAnalysisEngine**: Evaluates the email body for linguistic patterns associated with Business Email Compromise (BEC), such as urgency, financial requests ("wire transfer", "invoice"), and extracts embedded URLs for cross-correlation with the Advanced URL Intelligence Platform.
6. **AttachmentIntelligenceEngine**: Iterates through decoded MIME attachments, extracting metadata (filename, content type, size) and calculating cryptographic hashes (SHA-256) for IOC matching. Flags suspicious extensions (e.g., `.exe`, `.scr`).
7. **CampaignCorrelationEngine**: Correlates the current email's indicators (Sender, Subject) against known historical campaigns to detect widespread attacks.
8. **EmailRiskScoringEngine**: Normalizes the aggregated evidence into specific sub-scores (Authentication Risk, BEC Risk, Attachment Risk) yielding an Overall Risk Score and Threat Severity.
9. **EmailInvestigationOrchestrator**: The central asynchronous coordinator ensuring all engines execute systematically over the parsed EML structure.
10. **EmailAIIntegration**: Interfaces with the PHOENIX AI Brain to synthesize the technical findings into an Executive Summary and Threat Narrative suitable for incident responders.

### Frontend (`frontend/src/features/email-intelligence/`)
- **EmailInvestigationDashboard**: Central console for analysts to upload or paste raw email data.
- **HeaderExplorer**: Tabular viewer for standard and extended X-Headers.
- **AuthenticationDashboard**: Visual pass/fail state for SPF, DKIM, and DMARC alignment.
- **RoutingTimeline**: Visualizes the hop-by-hop `Received` chain from Origin to Destination.
- **ConversationViewer**: Analyzes the email body, highlighting extracted URLs and BEC urgency indicators.
- **AttachmentExplorer**: Lists attachment metadata, size, hashes, and highlights high-risk file types.
- **EmailAIFindings**: Presents the explainable AI narrative, summarizing the threat and recommending incident response actions.

## Data Models
New models added to `app/models/email_intelligence.py`:
- `EmailInvestigation`: Base relational store.
- `EmailHeaderData`: Sender, recipient, subject metadata.
- `AuthenticationResult`: SPF/DKIM/DMARC status.
- `RoutingHop`: Individual entries from the `Received` chain.
- `AttachmentMetadata`: File details and SHA256 hashes.
- `ExtractedURL`: URLs found within the email body.
- `CampaignCorrelation`: Historical campaign matches.

## Security & Scalability
The architecture supports incremental, memory-safe parsing of EMLs. The current implementation defers large binary storage (raw attachments) to external blob storage models, currently extracting and storing only actionable metadata and hashes in the PostgreSQL database for rapid querying and indicator matching.
