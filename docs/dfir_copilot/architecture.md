# Enterprise AI DFIR Copilot - Architecture Guide

## Overview
The AI DFIR Copilot (Phase X-050) provides a conversational intelligence layer over the Unified Forensic Timeline. It allows investigators to query complex temporal data and deeply nested artifacts using natural language.

## Architecture Components

### 1. Conversation Engine (`conversation_engine.py`)
Acts as the central router for user prompts. Depending on the `context_type` (e.g., TIMELINE vs ARTIFACT), it routes the query to specialized RAG (Retrieval-Augmented Generation) engines, formatting the final LLM response as a structured array of chunks.

### 2. Timeline Reasoning Engine (`timeline_reasoning.py`)
Specializes in extracting chronological sequences from the `mf_unified_events` table and reasoning over them. It is designed to strictly separate hard evidentiary facts from inferred AI assessments.

### 3. Artifact Explanation Engine (`artifact_explanation.py`)
Specializes in translating deeply technical artifacts (e.g., Windows Registry keys, Kubernetes manifest attributes) into plain English explanations of their significance, mapping them back to MITRE ATT&CK techniques where possible.

## Explainability Architecture
To prevent "hallucinations" from corrupting an investigation, the DFIR Copilot employs a rigid classification system for all AI outputs:
- `OBSERVATION`: A fact directly extracted from parsed evidence (e.g., "The file executed at 14:00").
- `ASSESSMENT`: An analytical conclusion inferred by the AI (e.g., "This suggests a spear-phishing attack").
- `RECOMMENDATION`: A suggested next step for the investigator.

These classifications are enforced at the API level (via Pydantic schemas) and rendered distinctly in the frontend UI via the `ExplanationBadge` component.

## Frontend Modules
- **DfirCopilotChat**: The primary interface. Supports multi-turn conversations and dynamic suggested next steps.
- **Context Panel**: A persistent sidebar that dynamically updates to show the specific evidence artifacts (via UUID) that the AI is currently reasoning about, allowing the analyst to verify the underlying data instantly.
