# Enterprise Cyber Operating System (CyberOS) Architecture

## 1. Overview
The Enterprise Cyber Operating System (CyberOS) (Phase X-100) is the capstone architectural layer of the PHOENIX X project. It serves as the unified operating foundation, orchestrating all previous 99 subsystems (SOC, DFIR, Threat Intel, Zero Trust, Cyber Command, etc.) into a cohesive, AI-native enterprise defense platform.

## 2. Core Components

### CyberOS Kernel
The central orchestration layer (`CyberOSKernel`). It handles module initialization, inter-process communication patterns, and global telemetry routing.

### Platform API Registry
A dynamic registry (`PlatformRegistryEntry`) where all underlying PHOENIX X modules register their capabilities and endpoints upon boot. This enables seamless service discovery across the enterprise.

### Unified Observability Engine
Tracks the health, API latency, and CPU/Memory usage of every registered module in real-time, ensuring the system maintains high availability and resilience.

### Unified AI Security Brain
The apex intelligence layer (`UnifiedAISecurityBrain`). It monitors the context of the active workspace and synthesizes cross-domain telemetry into actionable, explainable strategic guidance. 

## 3. Database Models

Implemented in `backend/app/models/cyber_os.py`:
- `PlatformRegistryEntry`: Dynamic tracking of module capabilities.
- `UnifiedObservabilityMetric`: Time-series logging of platform health and performance metrics.
- `GlobalSystemLog`: Aggregated event logging spanning the entire enterprise ecosystem.

## 4. API Endpoints

- `GET /api/v1/cyber-os/overview` - Retrieves the overarching CyberOS Kernel status.
- `GET /api/v1/cyber-os/registry` - Lists all dynamically registered PHOENIX X modules.
- `POST /api/v1/cyber-os/registry` - Endpoint for module self-registration during boot-up.
- `GET /api/v1/cyber-os/observability` - Real-time stream of global platform telemetry.

## 5. Frontend Interfaces

Module path: `frontend/src/features/cyberOS/`
- **CyberOSDesktop**: The root container layout providing a seamless, operating-system-like experience within the browser.
- **UnifiedNavigation**: Replaces siloed navigation bars with an apex command palette and universal cross-domain workspace switcher.
- **ObservabilityDashboard**: High-level visual tracking of system uptime, module registration, and API latency.
- **GlobalSearchInterface**: An omni-search overlay (`Cmd+K`) capable of querying the Knowledge Graph, Threat Intel, and Governance modules from anywhere.
- **UnifiedAIPanel**: A context-aware side panel representing the AI Security Brain. It adapts its guidance based on the current workspace (e.g., SOC vs Governance).

## 6. Security and Governance Integration
CyberOS enforces strict Zero Trust principles at the kernel layer. Inter-module communication requires authenticated service-to-service tokens. The Unified AI is governed strictly by the AI RMF guidelines; while it provides high-speed automated analysis and triage recommendations, all strategic actions mandate explicit human authorization through the Cyber Command layer.
