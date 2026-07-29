# Enterprise AI Threat Hunting Workspace - Architecture Guide

## Overview
The AI Threat Hunting Workspace (Phase X-034) is a proactive investigation platform. It allows security analysts to perform hypothesis-driven hunts across the entire enterprise data fabric. Unlike traditional log search tools, it leverages the AI Security Brain to suggest hypotheses and translate natural language into complex structured queries.

## Architecture Components

### 1. Threat Hunt Manager (`hunt_manager.py`)
Orchestrates the active hunt sessions. It manages state between queries, generated hypotheses, and correlated evidence, tying them all to a persistent `HuntSession` object.

### 2. Hypothesis Engine (`hypothesis_engine.py`)
A proactive AI module that observes the current hunt state (e.g., initial IOCs) and proposes plausible attack vectors. It generates a `HuntHypothesis` complete with a confidence score, MITRE ATT&CK mapping, and recommended follow-up queries.

### 3. Query Engine (`query_engine.py`)
Provides a dual-interface for searching:
- **Natural Language**: Translates human queries (e.g., "Show me lateral movement from HR") into structured Domain Specific Language (DSL).
- **Structured**: Accepts granular, boolean-driven queries for precise filtering across indices (EDR, Cloud, Network).

### 4. Pattern Discovery Engine (`pattern_discovery.py`)
Analyzes the bulk results returned by the Query Engine to identify anomalies, such as infrastructure reuse or temporal clustering, which an analyst might miss when manually reviewing logs.

### 5. Correlation Engine (`correlation_engine.py`)
Automatically cross-references artifacts found during a hunt with the Enterprise Knowledge Graph to identify links to known Threat Actors or historical Campaigns.

## Frontend Dashboard
The React frontend surfaces these advanced capabilities through specialized views:
- **ThreatHuntingDashboard**: Executive overview of hunt sessions, active hypotheses, and MITRE coverage.
- **HuntWorkspace**: The immersive interface where analysts execute Natural Language queries, review returned evidence, and accept AI-generated hypotheses from the sidebar.
- **QueryBuilder**: A structured interface for traditional Boolean log searching.
