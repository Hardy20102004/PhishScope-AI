# Enterprise Cloud & Container Forensics Platform - Architecture Guide

## Overview
The Cloud & Container Forensics Platform (Phase X-047) centralizes the investigation of ephemeral infrastructure. It processes Cloud Audit Logs (AWS CloudTrail), Kubernetes manifests, and Docker container metadata, integrating them into a unified cloud timeline.

## Architecture Components

### 1. Audit Engine (`audit_engine.py`)
Simulates parsing administrative identity events.
- Analyzes `AssumeRole`, `CreateAccessKey`, and policy changes.
- Automatically flags anomalies, such as long-term credentials being created by assumed roles originating from untrusted external IP addresses.

### 2. Container Engine (`container_engine.py`)
Analyzes the configuration state of Docker/Containerd workloads.
- Looks for severe misconfigurations that facilitate container escapes, specifically containers running with the `--privileged` flag or those that mount the host's root filesystem (`/`) or Docker socket (`/var/run/docker.sock`).

### 3. Kubernetes Engine (`kubernetes_engine.py`)
Analyzes Kubernetes cluster definitions and Pod manifests.
- Flags pods that attempt to break tenant isolation, such as those requesting `hostNetwork: true` (to sniff cluster traffic) or `hostPID: true` (to inspect host processes).

### 4. Timeline Builder (`timeline_builder.py`)
Synthesizes logs from the Audit, Container, and K8s engines into a single chronological view. This allows the investigator to trace an attack from the initial compromised IAM credential, through the deployment of a rogue K8s pod, to the execution of a privileged container escape.

## Frontend Modules
- **CloudDashboard**: Triage view for cloud environments, summarizing total audit events, container counts, and immediately alerting on IAM anomalies.
- **AuditLogViewer**: A searchable, chronological data grid for administrative actions, highlighting compromised identities in red.
- **ContainerExplorer**: Deep-dive view for individual container configurations. Clearly visualizes the `CMD` entrypoint and flags dangerous security contexts (e.g., Privileged mode or Hostfs mounts).
