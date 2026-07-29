# Enterprise Detection Gap Analysis Platform - Architecture Guide

## Overview
The Detection Gap Analysis Platform (Phase X-057) is the central intelligence hub for the Detection Engineering team. It continuously evaluates the enterprise's SIEM/EDR rule base against the MITRE ATT&CK framework to identify blind spots and prioritize engineering efforts.

## Architecture Components

### 1. Coverage Analysis Engine (`coverage_engine.py`)
Tracks the current detection success rate for specific MITRE Tactic/Techniques. It aggregates these individual metrics to provide the overall enterprise MITRE ATT&CK coverage percentage.

### 2. Gap Analysis Engine (`gap_analysis_engine.py`)
Identifies techniques where coverage falls below an acceptable threshold (e.g., < 30%). It automatically flags these as `DetectionGapRecord`s, assigning severities based on the severity of the gap (e.g., 0% coverage is CRITICAL).

### 3. Optimization Engine (`optimization_engine.py`)
Recommends specific engineering tasks to remediate the identified gaps. It translates a raw gap (e.g., "Missing coverage for T1562.001") into an actionable `ControlOptimizationPlan` (e.g., "Deploy new Splunk correlation search for Event ID 1102").

### 4. MITRE Mapping Engine (`mitre_mapping_engine.py`)
Provides the structural dictionary/mapping of tactics to techniques used by the other engines to ensure consistent alignment with the MITRE ATT&CK framework.

## Frontend Modules
- **DetectionGapDashboard**: High-level overview of overall detection coverage vs blind spots.
- **MitreCoverageHeatmap**: A visual, color-coded representation of the MITRE ATT&CK matrix to instantly identify weak areas.
- **OptimizationWorkspace**: A prioritized backlog for Detection Engineers, listing specific rules to write or tune based on the identified gaps.
