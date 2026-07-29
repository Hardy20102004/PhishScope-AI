# Enterprise Kubernetes Security & Container Runtime Defense Platform - Architecture Guide

## Overview
Phase X-063 introduces dedicated Cloud Native protection to PHOENIX X. The platform continuously monitors Kubernetes clusters across all major managed providers (EKS, AKS, GKE) and self-hosted environments. It provides deep visibility into complex RBAC identity relationships, validates admission policies, and ingests eBPF-driven container runtime events to secure the execution layer.

## Architecture Components

### 1. Cluster Discovery Engine (`cluster_discovery_engine.py`)
Connects to K8s API servers to inventory the cluster topology, extracting Nodes, Namespaces, Deployments, Pods, and ConfigMaps into standard relational models.

### 2. RBAC Analysis Engine (`rbac_analysis_engine.py`)
Untangles complex Kubernetes identity relationships. It resolves bindings between Subjects (Users, Groups, ServiceAccounts) and Roles/ClusterRoles, flattening them into an "Effective Permissions" matrix. It flags entities that violate the principle of least privilege (e.g., granting `*` on `*`).

### 3. Admission Policy Engine (`admission_policy_engine.py`)
Validates configurations before they are admitted into the cluster, ensuring Pod Security Standards (e.g., preventing privileged containers, enforcing read-only root filesystems) are met.

### 4. Container Runtime Engine (`container_runtime_engine.py`)
Ingests OS-level events from within running containers (via eBPF sensors), tracking container lifecycles, crashes, and anomalous process executions that indicate a runtime compromise.

### 5. K8s Risk Engine (`k8s_risk_engine.py`)
Aggregates identified RBAC violations, configuration flaws, and runtime anomalies to calculate a dynamic, holistic risk score for the entire cluster.

## Frontend Modules
- **ClusterDashboard**: A high-level, multi-cluster posture view aggregating risk scores across the cloud-native estate.
- **RBACDashboard**: An interactive permission matrix that clearly exposes "who can do what," immediately highlighting over-privileged ServiceAccounts.
- **NamespaceExplorer**: Groups workloads and network policies logically by namespace, providing developers and operators localized risk context.
- **ContainerRuntimeDashboard**: A live, terminal-style feed of container lifecycle events and runtime anomalies (like unexpected package installations).
