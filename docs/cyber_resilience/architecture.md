# Enterprise Cyber Resilience Scoring Platform - Architecture Guide

## Overview
The Cyber Resilience Scoring Platform (Phase X-058) is the executive abstraction layer of PHOENIX X. It ingests deep technical validation data from continuous validation, attack path simulations, and detection gap analysis, and translates it into high-level, board-ready metrics (KPIs), maturity assessments, and a single apex Cyber Resilience Score.

## Architecture Components

### 1. Security Scoring Engine (`scoring_engine.py`)
Aggregates technical sub-scores (Preventive Effectiveness, Detective Effectiveness, Response Effectiveness) using a weighted algorithm to generate the overarching `CyberResilienceScore`.

### 2. Maturity Assessment Engine (`maturity_engine.py`)
Evaluates raw operational data (e.g., MTTR, alert fidelity, BAS success rate) to automatically assign standard 5-tier maturity ratings (Initial -> Optimizing) to discrete security domains (SOC, DFIR, AppSec).

### 3. Executive KPI Engine (`kpi_engine.py`)
Tracks and logs specific Key Performance Indicators required for quarterly board reporting, such as Mean Time to Detect (MTTD), Mean Time to Contain (MTTC), and Phishing Simulation Failure Rates, along with their historical trends.

## Frontend Modules
- **CyberResilienceDashboard**: The highest-level executive view showing the overall resilience score and sub-pillar health.
- **SecurityMaturityRadar**: A visual radar/spider chart representing the 5-tier maturity status across all security domains.
- **ExecutiveKPIDashboard**: A simplified dashboard focusing strictly on the high-level operational metrics and ROI necessary for non-technical stakeholders.
