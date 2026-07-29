# Enterprise Email Forensics - Architecture Guide

## Overview
The Email Forensics Platform (Phase X-045) automates the most complex and error-prone aspect of Business Email Compromise (BEC) investigations: parsing SMTP headers to validate cryptographic signatures and trace the true origin of a message.

## Architecture Components

### 1. Message Parser (`message_parser.py`)
Extracts the fundamental components of an email container (EML/MSG). It separates the MIME body (HTML/Plain Text) from the raw header block, allowing downstream engines to operate on structured metadata rather than raw RFC 5322 strings.

### 2. Authentication Engine (`auth_engine.py`)
Parses the `Authentication-Results` header injected by modern MTAs (like Microsoft 365 or Google Workspace). It evaluates three critical protocols:
- **SPF** (Sender Policy Framework): Validates the originating IP against the domain's DNS records.
- **DKIM** (DomainKeys Identified Mail): Verifies the cryptographic hash of the email body has not been altered in transit.
- **DMARC** (Domain-based Message Authentication, Reporting, and Conformance): Verifies domain alignment (e.g., ensuring the `Return-Path` domain matches the visible `From` domain).

### 3. Routing Engine (`routing_engine.py`)
Parses the chain of `Received` headers. Because SMTP appends `Received` headers at the top of the message as it passes through MTAs, the engine reads them bottom-up, assigning a sequential `hop_index`. This allows analysts to visualize the exact path an email took across the internet.

## Frontend Modules
- **EmailDashboard**: Triage view for managing ingested EMLs and PSTs, highlighting containers that contain spoofed messages.
- **MessageViewer**: Renders the email body safely, alongside quick-glance badges indicating SPF/DKIM status.
- **HeaderAnalyzer**: A deeply technical view that visualizes the `Received` hop chain chronologically and explicitly breaks down exactly why an authentication check failed (e.g., "body hash did not verify").
