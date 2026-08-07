# PHOENIX X: AI Security Brain — Developer & API Integration Guide

## Overview
The AI Security Brain exposes a comprehensive REST API and Server-Sent Events (SSE) stream via `/api/v1/ai-brain` on the PHOENIX backend. All endpoints enforce strictly validated Pydantic V2 schemas and return detailed telemetry alongside investigative deductions.

---

## 1. Execute AI Orchestration
- **Endpoint**: `POST /api/v1/ai-brain/orchestrate`
- **Description**: Submits an analyst request or SIEM automated alert to the master `AIOrchestrator`. Automatically handles intent identification, context vault bundling, governance compliance checks, and multi-model failover execution.

### Request Payload (`OrchestrationRequest`)
```json
{
  "input_text": "Analyze observed phishing domain secure-update-apple-support.co.uk and correlate against historical indicators.",
  "capability": "Threat Analysis",
  "case_id": "8a09b301-c81b-4f7f-a2e2-9b2f30501a33",
  "tenant_id": "enterprise_tenant_01",
  "override_model_id": "claude-3-5-sonnet",
  "additional_context": {
    "evidence": [
      {
        "id": "EVID-0001",
        "type": "domain",
        "value": "secure-update-apple-support.co.uk",
        "reputation_score": "Critical Phishing (Score: 94)"
      }
    ],
    "policies": [
      "Block all newly registered domains exhibiting homogamy tactics."
    ]
  }
}
```

### Response Payload (`OrchestrationResponse`)
```json
{
  "request_id": "AI-REQ-88710B4F3A",
  "response_text": "### Technical Analysis\nThe target domain exhibits characteristic homogamy phishing strategies...",
  "provider_used": "claude",
  "model_used": "claude-3-5-sonnet",
  "confidence_score": 0.94,
  "evidence_references": [
    {
      "finding_id": "EVID-0001",
      "target": "secure-update-apple-support.co.uk",
      "verified_in_vault": true
    }
  ],
  "hallucination_indicators_detected": [],
  "decision_trace": [
    {
      "step_number": 1,
      "step_name": "Evidence Vault Correlation",
      "rationale": "Analyzed 1 evidence records to establish cross-indicator linkage.",
      "confidence": 0.6,
      "output": "Correlated 1 indicators across 1 distinct vectors (1 flagged high-risk)."
    },
    {
      "step_number": 2,
      "step_name": "Bayesian Confidence Calculation",
      "rationale": "Computed synthesized confidence score across evidence density.",
      "confidence": 0.94,
      "output": "Pipeline synthesis finalized successfully."
    }
  ],
  "token_usage": {
    "input_tokens": 420,
    "output_tokens": 180,
    "cost_usd": 0.00396
  },
  "latency_ms": 680,
  "policy_status": "PASSED"
}
```

---

## 2. Real-Time Streaming Inference
- **Endpoint**: `POST /api/v1/ai-brain/stream`
- **ContentType**: `text/event-stream` (Server-Sent Events)
- **Description**: Streams generated inference text and trace reasoning markers directly to client user interfaces in real-time, dramatically improving analyst experience during long multi-step deductive investigations.

---

## 3. Telemetry, Providers, and Capabilities
- `GET /api/v1/ai-brain/health-analytics`: Returns live circuit-breaker health, 24-hour token metrics, dollar cost accounting, and governance interception statistics.
- `GET /api/v1/ai-brain/providers`: Returns live failover engine states for configured providers.
- `GET /api/v1/ai-brain/models`: Returns enterprise model catalog, context limits, and per-token pricing structures.
- `GET /api/v1/ai-brain/capabilities`: Returns standard SOC operational tasks and mapped models.
- `DELETE /api/v1/ai-brain/memory/{session_id}`: Purges an interactive diagnostic dialogue session from active memory.
