# Enterprise Threat Timeline Intelligence Architecture

## Overview
The Enterprise Threat Timeline Intelligence Platform serves as the chronological backbone of PHOENIX X. It automatically builds, normalizes, and reconstructs evidence-backed timelines by correlating disparate events across the Knowledge Graph, IOC Engine, and Cloud federations.

## Core Components

### 1. Timeline Manager & DB Models
Provides the storage and retrieval mechanics.
- **`Timeline`**: A logical grouping of events (e.g., Campaign, Threat Actor, Investigation).
- **`TimelineEvent`**: Standardized occurrence record, tied to a strict UTC timestamp and a specific `EventCategory`.
- **`EventEvidence`**: External validation links (e.g., PCAPs, alerts) tied to events for explainability.

### 2. Event Normalization Engine
- Ingests raw data (e.g., STIX bundles, syslog strings) and parses arbitrary date formats into a strict timezone-aware UTC format.
- Standardizes observation categories (`CREATION`, `COMMUNICATION`, `EXECUTION`).

### 3. Event Correlation Engine
- Analyzes newly ingested events and automatically groups them into existing timelines based on temporal proximity and shared entity IDs derived from the Knowledge Graph.

### 4. Historical Reconstruction Engine
- Identifies gaps in intelligence (e.g., observing execution but missing delivery).
- Automatically generates "Hypothetical" events (`is_hypothetical=True`) with adjusted confidence scores to visually represent assumed historical occurrences.

### 5. Timeline Analytics Engine
- **Heatmaps**: Aggregates event density over time (e.g., daily counts) to spot peak activity windows.
- **Duration Tracking**: Computes total lifespan of a campaign or infrastructure from first to last observation.

### 6. Visualization UI
- Glassmorphism-styled React dashboards (`TimelineDashboard` & `TimelineExplorer`) that render the chronological narrative. It distinguishes hypothetical AI inferences from confirmed intelligence using specific visual cues (e.g., dashed borders).
