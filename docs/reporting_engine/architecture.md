# Enterprise Automated Forensic Reporting - Architecture Guide

## Overview
The Automated Forensic Reporting Platform (Phase X-049) is the authoritative output module of PHOENIX X. It compiles findings from all underlying modules into structured, human-readable, and legally defensible documents.

## Architecture Components

### 1. Chain of Custody Engine (`custody_engine.py`)
Maintains an immutable ledger for all evidence handled by PHOENIX X. 
- Every time evidence is ingested, transferred, analyzed, or archived, a `ChainOfCustodyRecord` is appended.
- Each record calculates a cryptographic hash that relies on the context of the action, ensuring the ledger cannot be silently altered or reordered.

### 2. Report Manager (`report_manager.py`)
Orchestrates the creation of reports.
- It scaffolds reports using predefined templates (e.g., scaffolding an `EXECUTIVE_SUMMARY` and `OBSERVED_EVIDENCE` section when a new "Court-Ready" report is requested).

### 3. Traceability Engine (`traceability_engine.py`)
Ensures that analytical claims are grounded in fact.
- Every `ReportSection` maintains a JSON list of `linked_evidence_ids`. This guarantees that if a report states "Malware was executed at 14:00 UTC", there is a direct database link back to the specific Disk Image MFT record that proves it.

### 4. Generation Engine (`generation_engine.py`)
Handles the finalization of a report.
- Once an analyst finalizes a report, this engine locks the record and generates a simulated Digital Signature (SHA-256 hash of the content, author, and timestamp) to prove the document has not been tampered with post-generation.

## Frontend Modules
- **ReportingDashboard**: Central hub for managing all draft and finalized reports across investigations.
- **ChainOfCustodyViewer**: A chronological, tamper-evident ledger view proving the integrity of a single piece of evidence.
- **CourtReadyPreview**: A highly stylized, read-only document view that clearly separates traceble evidentiary observations from analytical assessments, complete with a digital signature watermark.
