# Enterprise SOC Collaboration Workspace - Architecture Guide

## Overview
The SOC Collaboration Platform (Phase X-037) serves as the central communication and knowledge-sharing hub for analysts across all modules. It unifies isolated workflows (Hunting, Alert Triage, Incident Response) by providing persistent, auditable chat rooms and shared evidence notes.

## Architecture Components

### 1. Workspace Manager (`workspace_manager.py`)
Manages the lifecycle of a `CollabWorkspace`. These workspaces can be general-purpose or strictly linked to a specific entity like a `DFIRCase` or `HuntSession`.

### 2. Messaging Service (`messaging_service.py`)
Handles the persistence of `ChatMessage` objects within a workspace. Currently built using a REST polling design pattern to maintain compatibility with the core stateless SQLAlchemy + FastAPI architecture, avoiding complex WebSocket overhead for the MVP.

### 3. Knowledge Engine (`knowledge_engine.py`)
Manages `AnalystNote` objects. These are markdown-formatted playbooks, SOPs, or investigation summaries that can be pinned to a workspace or searched globally.

### 4. Workload Manager (`workload_manager.py`)
Tracks `AnalystPresence`. It calculates current team bandwidth (active cases, online status) to assist Incident Commanders in optimally assigning new cases.

### 5. AI Collab Assistant (`ai_collab_assistant.py`)
Provides real-time AI capabilities directly in chat rooms, such as summarizing long incident threads for newly assigned analysts.

## Database Schema Highlights
- **`CollabWorkspace`**: The logical chat/collaboration room.
- **`ChatMessage`**: Auditable text objects bound to a workspace.
- **`AnalystNote`**: Reusable markdown documents.
- **`AnalystPresence`**: Real-time tracker for team workload metrics.

## Frontend Modules
- **TeamDashboard**: Executive command center viewing online presence and cross-team workload distribution.
- **WorkspaceRoom**: The Slack-like interface for real-time incident threading, featuring an AI context sidebar.
- **KnowledgeCenter**: The centralized repository for all `AnalystNote` objects, facilitating cross-team SOP sharing.
