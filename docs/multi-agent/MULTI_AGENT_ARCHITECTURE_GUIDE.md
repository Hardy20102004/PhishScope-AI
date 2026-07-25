# PHOENIX X Multi-Agent Architecture Guide

The Multi-Agent AI Framework is the crowning achievement of PHOENIX X, built directly on top of the AI Security Brain (Phase X-001). It transforms the platform from a single intelligence node into a distributed, collaborative workforce of autonomous cybersecurity specialists.

## 1. Core Paradigm

Instead of monolithic prompts attempting to solve complex investigations in a single pass, the Multi-Agent Framework utilizes **Task Decomposition and Asynchronous Directed Acyclic Graphs (DAGs)**.

The framework is composed of:
*   **AgentRegistry & AgentManager**: Tracks capabilities and instantiates the workforce.
*   **Specialized Agents**: 14 distinct subclasses of `AbstractSecurityAgent` (e.g. `InvestigatorAgent`, `MalwareAnalysisAgent`, `ThreatIntelAgent`).
*   **Task Planner**: Detects intent and generates the execution DAG.
*   **Execution Engine**: Resolves DAG dependencies and runs tasks concurrently via `asyncio`.
*   **Conflict Resolver**: Automatically synthesizes disparate findings and detects contradictions.

## 2. Agent Composition

Every agent wraps the foundational `AIOrchestrator` but imposes narrow, focused prompts and restricted memory contexts.

```python
class ThreatIntelAgent(AbstractSecurityAgent):
    def get_system_prompt(self) -> str:
        return "You are a Tier 3 Threat Intelligence Specialist. Correlate IOCs against global databases."
```

## 3. Communication Bus

Agents do not execute in silos; they collaborate using the `CommunicationBus`. 
Supported interaction patterns:
*   **POINT-TO-POINT (Handoff)**: Agent A finishes and directly passes context to Agent B.
*   **BROADCAST**: Agent A announces a critical finding (e.g. "Domain Fast-Flux detected") to all active agents.

## 4. 7-Tier Shared Memory Topology

To prevent context collapse and ensure long-term retention, agents share memory across 7 tiers:
1.  **Working Memory (Scratchpad)**: Fast, volatile memory for mid-task reasoning.
2.  **Evidence Memory**: Immutable storage for confirmed artifacts (PCAPs, Hashes).
3.  **Conversation Memory**: History of user interaction.
4.  **Case Memory**: The complete dossier for a specific investigation.
5.  **Organization Memory**: Tenant-specific baselines and historical context.
6.  **Temporary Memory**: Automatically purged post-execution.
7.  **Persistent Memory**: Long-term model tuning data.

## 5. Security & Isolation

The `AgentSecurityEnforcer` ensures Zero-Trust execution:
*   **RBAC**: Tier 1 analysts cannot trigger containment agents.
*   **Zero-Data-Leakage**: PII and secrets are scrubbed before payload transmission to the underlying orchestrator.
*   **Prompt Protection**: All inputs are sanitized against OWASP LLM01 heuristics.
