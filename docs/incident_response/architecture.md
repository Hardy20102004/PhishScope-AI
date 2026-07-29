# Enterprise Incident Response & Case Management - Architecture Guide

## Overview
The Incident Response (IR) Platform (Phase X-035) manages the full lifecycle of a security incident, transitioning an event from an initial alert into a structured, trackable case. It is designed to be DFIR-ready (Digital Forensics and Incident Response), emphasizing evidence integrity and immutable auditing.

## Architecture Components

### 1. Incident Manager (`incident_manager.py`)
Handles the high-level state machine of an incident (NEW -> INVESTIGATING -> CONTAINMENT -> RESOLVED -> CLOSED). When an incident is declared, it automatically provisions a default `DFIRCase` workspace.

### 2. Evidence Manager (`evidence_manager.py`)
The core of the DFIR capabilities. It manages `EvidenceRecord`s and enforces an immutable `ChainOfCustodyLog`. Whenever evidence is attached or transferred, a SHA-256 digital signature of the artifact is calculated and appended to the ledger to guarantee against tampering.

### 3. Task Manager (`task_manager.py`)
Provides Kanban-style tracking for response actions (e.g., Containment, Forensics). Tasks can be assigned to specific analysts and tracked via due dates.

### 4. Reporting Engine (`reporting_engine.py`)
Leverages the AI Context Engine to read through all attached evidence, tasks, and notes, automatically drafting a natural-language Executive Incident Summary.

## Database Schema Highlights
- **`Incident`**: The overarching event.
- **`DFIRCase`**: A specialized sub-workspace within an incident. (An incident might have multiple cases, e.g., one for Malware Analysis, one for Cloud Forensics).
- **`EvidenceRecord`**: The digital artifact itself.
- **`ChainOfCustodyLog`**: Bound one-to-many from `EvidenceRecord`. Immutable.
- **`IncidentTask`**: Action items mapped to the incident.

## Frontend Dashboard
- **SOCDashboard**: Executive view of MTTR (Mean Time to Respond) and active incident queues.
- **IncidentWorkspace**: The primary hub for managing a specific incident, featuring AI Summaries and recent task status.
- **EvidenceLocker**: A specialized view showcasing the ledger of evidence and its associated Chain of Custody signatures.
- **TaskBoard**: A drag-and-drop Kanban board for task orchestration.
