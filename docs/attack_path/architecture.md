# Enterprise AI Attack Path Simulation Platform - Architecture Guide

## Overview
The Attack Path Simulation Platform (Phase X-056) uses graph theory to proactively identify structural weaknesses in the enterprise environment. By mapping assets as nodes and permissions/network paths as edges, it simulates how an attacker could move laterally toward critical assets.

## Architecture Components

### 1. Graph Engine (`graph_engine.py`)
Manages the foundational data structure. Assets (Users, Endpoints, IAM Roles) are ingested and represented as Nodes. The complex web of trust relationships, network routes, and administrative privileges are represented as directed Edges.

### 2. Exposure Engine (`exposure_engine.py`)
The pathfinding core. It uses graph traversal algorithms (e.g., Breadth-First Search, Dijkstra's) to find viable routes between a low-privileged starting point (e.g., a phished user) and a high-value target (e.g., a domain controller).

### 3. Blast Radius Engine (`blast_radius_engine.py`)
Calculates downstream impact. If a specific node is compromised, this engine traverses outward to enumerate all reachable assets, helping prioritize containment during a live incident.

### 4. Remediation Prioritization Engine (`remediation_engine.py`)
Unlike traditional vulnerability management that produces endless lists, this engine uses graph centrality metrics to identify "Choke Points." Severing a single high-centrality edge (e.g., enforcing MFA on one specific jump host) can sever hundreds of viable attack paths simultaneously.

## Frontend Modules
- **AttackPathDashboard**: High-level exposure metrics and top critical assets at risk.
- **InteractiveAttackGraph**: Visual traversal of simulated attack paths.
- **BlastRadiusViewer**: Impact estimation for compromised nodes.
- **RemediationWorkspace**: The prioritized list of choke points yielding the highest return on engineering investment.
