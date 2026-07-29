# Enterprise SOC Digital Twin - Architecture Guide

## Overview
The Digital Twin Platform (Phase X-040) is a continuous improvement engine that allows SOC architects and CISOs to model "what-if" operational scenarios. By altering variables such as Alert Volume, Analyst Headcount, and Automation Rates, users can forecast SLA breaches and MTTR spikes before they occur in the real world.

## Architecture Components

### 1. Simulation Engine (`simulation_engine.py`)
Utilizes a deterministic queueing theory model to estimate the impact of workload (alert volume) versus capacity (headcount * automation). When utilization surpasses 100%, the engine mathematically forecasts exponential degradation in MTTR and SLA compliance.

### 2. Capacity Engine (`capacity_engine.py`)
A predictive microservice that calculates exact hiring requirements needed to bring forecasted utilization back down to a healthy baseline (typically 80%).

### 3. Optimization Engine (`optimization_engine.py`)
Acts as the AI consultant. When a `SimulationResult` indicates a bottleneck (e.g., utilization > 90%), this engine generates strategic `OptimizationRecommendation` objects suggesting specific playbook deployments or staffing adjustments.

## Database Schema Highlights
- **`SimulationScenario`**: Defines the independent variables (Volume Multiplier, Headcount).
- **`SimulationResult`**: The dependent variables calculated by the engine (Forecasted MTTR, Utilization).
- **`OptimizationRecommendation`**: Strategic mitigation plans tied to a specific result.

## Frontend Modules
- **ScenarioPlanner**: Interactive UI with sliders to define the simulation variables.
- **SimulationWorkspace**: Visualizes the calculated results, warning the user of potential queueing failures.
- **OptimizationDashboard**: Presents the AI-generated recommendations to solve identified capacity constraints.
