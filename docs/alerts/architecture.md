# Enterprise Security Alert Management Platform - Architecture Guide

## Overview
The Enterprise Security Alert Management Platform (Phase X-031) is the central nervous system for SOC operations within PHOENIX X. It provides real-time ingestion, normalization, enrichment, and correlation of alerts from disparate security tools (EDR, SIEM, NDR, Firewalls).

## Architecture Components

### 1. Alert Ingestion Engine (`ingestion.py`)
Provides a highly scalable webhook receiver and API endpoint for external systems. It validates incoming payloads, orchestrates normalization, and dispatches background tasks for asynchronous processing without blocking the client.

### 2. Alert Normalization Engine (`normalization.py`)
Translates vendor-specific schemas (e.g., Splunk, CrowdStrike) into the unified PHOENIX X `Alert` schema. It extracts and standardizes Indicators of Compromise (IOCs) such as IPs, Domains, and Hashes into `AlertEvidence` records.

### 3. Deduplication Engine (`deduplication.py`)
Reduces alert fatigue by suppressing noisy, repetitive alerts within a configurable time window. It matches incoming alerts against recent alerts based on `source_alert_id` or similarity heuristics.

### 4. Prioritization Engine (`prioritization.py`)
Dynamically calculates Risk, Confidence, and Priority scores. It combines statically mapped severity levels with organizational Asset Criticality and Evidence Quality to prioritize the analyst queue.

### 5. Enrichment Engine (`enrichment.py`)
Leverages the AI Brain and Threat Intelligence feeds to automatically add context to an alert. It maps alerts to MITRE ATT&CK techniques and generates a natural language `ai_summary` to guide investigations.

### 6. Correlation Engine (`correlation.py`)
Groups isolated alerts into `AlertCorrelationGroup`s based on shared infrastructure, identical IOCs, or related threat actors. This significantly reduces the total number of cases an analyst must review.

### 7. Assignment & Audit Engines (`assignment.py`, `audit.py`)
Manages the distribution of alerts to analysts and maintains an immutable cryptographic-style chronological ledger (`AlertLifecycleEvent`) of every state change or comment made during an investigation.

## Frontend
The platform includes a modern, high-performance React frontend featuring:
- **SOC Dashboard**: High-level telemetry, MTTA/MTTR metrics, and priority distributions.
- **Alert Queue**: The primary workspace for triage with advanced filtering and dynamic styling.
- **Alert Detail**: A deep-dive view into a specific alert's evidence, AI summary, and audit trail.
- **Correlation Explorer**: Visual representation of grouped alerts and shared indicators.
