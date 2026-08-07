# Enterprise AI Alert Triage & Prioritization Platform - Architecture Guide

## Overview
The AI Alert Triage Platform (Phase X-033) sits atop the Alert Management Platform. Its primary purpose is to dramatically reduce alert fatigue by clustering related events into `AITriageGroup`s and intelligently prioritizing them based on real-world business impact.

## Architecture Components

### 1. Alert Grouping Engine (`grouping.py`)
Replaces basic deterministic correlation with fuzzy logic. It evaluates time windows, shared MITRE paths, and infrastructure links to group alert storms or multi-stage attacks into a single triage unit.

### 2. Business Impact Engine (`business_impact.py`)
Queries the `AssetBusinessContext` (a proxy for a CMDB) to determine the criticality and data sensitivity of the target asset. This shifts the focus from "How bad is the malware?" to "How bad is it *if it executes on this specific server*?".

### 3. Priority Engine (`priority.py`)
Calculates the final `priority_tier` using the formula:
`Priority = (Threat_Severity * 0.6 + Business_Impact * 0.4) * AI_Confidence`.
This ensures that highly confident, high-impact alerts surface to the top of the queue.

### 4. Recommendation Engine (`recommendation.py`)
Acts as the bridge to the AI Security Brain (Explainable AI). It generates natural language summaries, explains the priority justification, and provides concrete, evidence-backed next steps for the analyst.

### 5. Feedback Learning Engine (`feedback.py`)
A continuous learning loop. When an analyst disagrees with the AI (e.g., marks an `AITriageGroup` as a False Positive or overrides the Priority), the feedback is recorded in `AnalystFeedback`. This data is staged for asynchronous consumption by ML training pipelines to improve future grouping and priority predictions.

## Frontend
The React frontend surfaces the advanced capabilities through specialized views:
- **AITriageDashboard**: Tracks the efficiency of the pipeline (Alert Reduction %, Feedback Rate).
- **GroupedAlertsQueue**: The primary workspace, replacing the raw alert feed.
- **TriageDetail**: An immersive investigation view highlighting the AI's recommendations, uncertainty factors, and a built-in feedback submission loop.
