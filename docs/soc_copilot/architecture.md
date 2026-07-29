# Enterprise AI SOC Copilot - Architecture Guide

## Overview
The AI SOC Copilot (Phase X-039) serves as an omniscient, centralized assistant. Unlike the legacy `copilot` module (which tightly bound conversations to a single Incident ID), the `soc_copilot` module is completely decoupled, enabling global threat hunting, generic knowledge graph queries, and cross-incident executive reporting.

## Architecture Components

### 1. Conversation Engine (`conversation_engine.py`)
Manages the orchestration of multi-turn chat sessions. It acts as the controller, receiving user input, dispatching it to the Reasoning Engine, and persisting both the User's query and the AI's response to the database.

### 2. Reasoning Engine (`reasoning_engine.py`)
The "brain" of the Copilot. It enforces a strict chain-of-thought process that inherently separates factual observed evidence (from RAG/Knowledge Graph) from the AI's analytical assessment, creating an auditable `CopilotReasoningLog` for every response.

### 3. Evidence Retrieval Engine (`evidence_retrieval.py`)
Interfaces with the Enterprise RAG (Retrieval-Augmented Generation) systems and Knowledge Graph to fetch real-time context to ground the AI's responses and reduce hallucination.

### 4. Context Engine (`context_engine.py`)
Silently observes the user's UI state (e.g., "User is currently viewing the Executive Dashboard") and injects this context as a hidden System Prompt to tailor the AI's tone and technical depth.

## Database Schema Highlights
- **`CopilotSession`**: The overarching chat room.
- **`CopilotChatMessage`**: User and AI dialog turns.
- **`CopilotReasoningLog`**: Crucial for Explainable AI (XAI). This table forces the LLM to log its cited evidence and confidence score independently from the final markdown text it shows the user.

## Frontend Modules
- **CopilotWorkspace**: The primary conversational interface.
- **ContextPanel**: A sidebar that transparently displays the RAG citations and Knowledge Graph nodes the AI used to formulate its current answer, building analyst trust.
- **SuggestedPrompts**: Dynamically generated next actions (e.g., "Isolate Host", "Draft Report") based on the current context.
