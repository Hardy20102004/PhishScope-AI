# Enterprise Breach & Attack Simulation (BAS) Platform - Architecture Guide

## Overview
The BAS Platform (Phase X-051) is a specialized module for safely validating the effectiveness of enterprise security controls. Rather than running unconstrained offensive exploits, this platform orchestrates "safe" behavioral tests and programmatically queries integrated defense systems (SIEM, EDR) to verify if the behavior was detected.

## Architecture Components

### 1. Simulation Manager (`simulation_manager.py`)
Responsible for managing `BasScenario` templates and orchestrating the lifecycle of a `BasSimulation`. It handles state transitions (PENDING -> RUNNING -> COMPLETED) and safely dispatches simulation steps.

### 2. Validation Engine (`validation_engine.py`)
The core verification module. After a simulation step executes, this engine polls the APIs of integrated security tools (e.g., CrowdStrike, Splunk) to determine if a corresponding alert was generated. The results are stored in `BasValidationResult`.

### 3. Scoring Engine (`scoring_engine.py`)
Upon completion of a simulation, this engine calculates an overall "Security Readiness Score" based on the ratio of detected actions versus missed actions.

### 4. MITRE Coverage Engine (`mitre_coverage_engine.py`)
Aggregates validation data across all historical simulations, mapping the results back to MITRE ATT&CK tactics to generate organizational heatmaps.

## Safety & Compliance
By design, the BAS Platform separates the execution of test events from the validation of those events. It focuses strictly on verifiable evidence of detection (e.g., capturing a SIEM Alert ID) rather than offensive compromise.
