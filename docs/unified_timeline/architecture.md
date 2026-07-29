# Enterprise Unified Forensic Timeline - Architecture Guide

## Overview
The Unified Forensic Timeline (Phase X-048) is the capstone of the PHOENIX X architecture. It acts as a normalization layer, ingesting disparate forensic artifacts (Email headers, Disk MFT records, Memory network connections, Cloud audit logs) and weaving them into a single, cohesive narrative.

## Architecture Components

### 1. Data Normalization (`UnifiedTimelineEvent`)
Instead of duplicating massive payloads from individual modules, the timeline uses a polymorphic referencing schema. Each event stores a `source_module` (e.g., `EMAIL`), a `source_table`, and a `source_id`. It extracts just enough JSON metadata (`render_metadata`) to display the event in the UI without requiring expensive JOINs back to the original database tables.

### 2. Correlation Engine (`correlation_engine.py`)
Automatically scans the normalized timeline for shared Indicators of Compromise (IOCs).
- **Example**: If the Memory Forensics module detects a beacon to `203.0.113.5`, and the Cloud Forensics module detects an `AssumeRole` call originating from `203.0.113.5`, the Correlation Engine creates an explicit, high-confidence link between those two events.

### 3. Relationship Engine (`relationship_engine.py`)
Infers causality based on temporal proximity and context.
- **Example**: If an email with an attachment named `invoice.exe` is received, and 3 minutes later a file creation event for `invoice.exe` occurs on Disk, the engine infers a `CAUSAL_SPAWN` relationship, visually demonstrating that the email *caused* the file drop.

## Frontend Modules
- **UnifiedTimelineDashboard**: Executive-level view of the correlation session, summarizing the number of modules involved and the density of the attack timeline.
- **ChronologicalExplorer**: A highly optimized, vertically scrolling UI that seamlessly interweaves events from different modules based on their strict UTC timestamps.
- **CorrelationGraph**: A visual mapping tool that explicitly draws links between distinct events that share IPs, Hashes, or causal chains, allowing analysts to instantly pivot across domains.
