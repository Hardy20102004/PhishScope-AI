# Enterprise SOC Executive Dashboard - Architecture Guide

## Overview
The Executive Dashboard (Phase X-038) translates technical, granular SOC data into strategic, business-aligned intelligence. It provides the CISO and SOC Management with macro-level insights, risk posture analysis, and AI-generated board reports.

## Architecture Components

### 1. Analytics Engine (`analytics_engine.py`)
Computes top-level KPIs such as MTTR (Mean Time to Resolve), MTTA (Mean Time to Acknowledge), and Incident Volume trends. To ensure dashboard performance, these metrics should be pre-calculated daily into the `ExecutiveMetric` rollup table rather than querying millions of raw alerts in real-time.

### 2. Risk Engine (`risk_engine.py`)
Evaluates the macro security posture by analyzing the `BusinessRiskScore`. It correlates open, unmitigated CVEs and active threat campaigns against critical Business Units (e.g., Finance, HR) to generate high-level heatmaps.

### 3. AI Executive Assistant (`ai_executive_assistant.py`)
Uses the enterprise AI framework to parse raw KPIs and generate plain-english, strategic `ExecutiveReport` documents suitable for non-technical Board Members.

## Database Schema Highlights
- **`ExecutiveMetric`**: Time-series rollup table for fast rendering of KPI charts.
- **`BusinessRiskScore`**: Tracks calculated risk per business unit over time.
- **`ExecutiveReport`**: Stored markdown objects representing monthly/weekly summaries.

## Frontend Modules
- **CISODashboard**: The overarching executive view featuring AI summaries and the Business Risk Map.
- **OperationalMetrics**: A specialized drill-down for SOC Managers to track SLA compliance and analyst velocity.
- **RiskPosture**: Visualizes enterprise-wide MITRE ATT&CK coverage gaps and active unmitigated threat exposures.
