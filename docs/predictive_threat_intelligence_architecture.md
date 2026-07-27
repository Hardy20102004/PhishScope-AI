# Enterprise Predictive Threat Intelligence Architecture

## Overview
The Enterprise Predictive Threat Intelligence Platform shifts PHOENIX X from a reactive posture to a proactive posture. By constantly scanning the Enterprise IOC Knowledge Graph and the Threat Timeline Intelligence Engine, the system identifies historical patterns and uses them to forecast emerging campaigns, infrastructure reuse, and threat actor behavioral shifts.

## Core Components

### 1. Prediction Manager & Models
Handles the persistence of predictive data.
- **`ThreatForecast`**: The core prediction object, linked to a specific domain (e.g., `INFRASTRUCTURE_REUSE`, `CAMPAIGN_EVOLUTION`).
- **`ForecastScenario`**: Allows for probabilistic branching (e.g., Scenario A at 75%, Scenario B at 25%).
- **`ForecastEvidence`**: Explicit links mapping the prediction back to raw data nodes in the Knowledge Graph or events in the Timeline Engine.

### 2. Pattern Discovery Engine
A heuristic scanning engine that looks for specific motifs in the Knowledge Graph. 
- Example: Detects if a previously dormant, known-malicious domain (linked to APT29) suddenly receives a new TLS certificate. This pattern suggests imminent staging for a new campaign.

### 3. Forecast Engine
Takes the raw patterns discovered by the Pattern Engine and compiles them into structured `ThreatForecast` objects, generating the alternative scenarios, computing the confidence scores, and defining the time horizon (e.g., 14 days).

### 4. Trend Analysis Engine
Computes macro-level trends across the entire enterprise intelligence corpus.
- Aggregates `TARGETS` relationships over time to determine if a specific industry (e.g., Healthcare) is seeing a surge in attacks.
- Provides time-series projections for malware volume (e.g., Ransomware vs. Infostealer).

### 5. API & Background Execution
Predictions are computationally expensive as the graph grows. The Forecast Engine is triggered via the `/forecasts/generate` endpoint, which offloads the pattern discovery and generation logic to asynchronous background tasks.

### 6. Interactive Dashboards
A specialized suite of React components (`PredictionDashboard`, `ForecastExplorer`, `TrendDashboard`) built with the premium glassmorphism design system. It allows analysts to visualize alternative scenarios and trace predictions back to the underlying evidence.
