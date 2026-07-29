# Enterprise Blue Team Readiness Platform - Architecture Guide

## Overview
The Blue Team Readiness Platform (Phase X-053) is the central metric aggregator for enterprise defensive operations. Rather than managing alerts directly, this platform evaluates *how well* the organization manages alerts and maintains detection fidelity.

## Architecture Components

### 1. Detection Validation Engine (`detection_validation.py`)
Analyzes the historical performance of SIEM/EDR rules. It categorizes rules into `HEALTHY`, `NOISY` (e.g., >80% False Positive rate), or `BROKEN` (0 true or false positives over an extended period).

### 2. Analyst Readiness Engine (`analyst_readiness.py`)
Calculates operational efficiency metrics (MTTT, MTTR, Playbook Adherence). To prevent punitive individual targeting, metrics are aggregated at the *Team Level* (e.g., SOC Tier 1, DFIR) to assess overall maturity.

### 3. Maturity Engine (`maturity_engine.py`)
The synthesizer. It weights the discrete metrics (Detection Health and Analyst Readiness) alongside Purple Team validation outcomes (from BAS and Red Team campaigns) to generate a single, overarching **Operational Maturity Score**.

## Frontend Modules
- **BlueTeamDashboard**: The high-level executive summary displaying the overall Operational Maturity Score.
- **DetectionHealthDashboard**: A specialized workspace for Detection Engineers to identify and prioritize noisy rules for tuning.
- **AnalystReadinessDashboard**: Operational tracking of SOC tier efficiency.
- **PurpleTeamMetrics**: A critical correlation view showing how external validation exercises directly lead to internal defensive improvements.
