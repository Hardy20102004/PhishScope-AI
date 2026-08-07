from typing import Any, Dict, List, Optional

import structlog

from app.models.ai_brain import ModelHealthStatus

logger = structlog.get_logger("phoenix.ai_brain.registry")

class ModelRegistry:
    """
    Enterprise Model Registry maintaining exhaustive metadata, live health telemetry,
    cost accounting metrics, and context window limits for every AI model.
    """
    def __init__(self):
        self._models: Dict[str, Dict[str, Any]] = {}
        self._seed_default_models()

    def _seed_default_models(self):
        defaults = [
            {
                "model_id": "claude-3-5-sonnet",
                "provider": "claude",
                "display_name": "Claude 3.5 Sonnet",
                "version": "2024-10-22",
                "max_context_tokens": 200000,
                "max_output_tokens": 8192,
                "supported_languages": ["en", "es", "fr", "de", "ja", "zh"],
                "cost_per_1k_input": 0.003,
                "cost_per_1k_output": 0.015,
                "typical_latency_ms": 750,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Reasoning", "Threat Analysis", "Report Writing", "Threat Hunting", "IOC Correlation"]
            },
            {
                "model_id": "gemini-3.1-pro",
                "provider": "gemini",
                "display_name": "Google Gemini 3.1 Pro (High)",
                "version": "3.1-2026",
                "max_context_tokens": 2000000,
                "max_output_tokens": 8192,
                "supported_languages": ["en", "es", "fr", "de", "ja", "zh", "pt", "ru"],
                "cost_per_1k_input": 0.0035,
                "cost_per_1k_output": 0.0105,
                "typical_latency_ms": 650,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Summarization", "Threat Analysis", "Evidence Explanation", "Timeline Generation", "Risk Assessment"]
            },
            {
                "model_id": "gpt-4o",
                "provider": "openai",
                "display_name": "OpenAI GPT-4o Omni",
                "version": "2024-08-06",
                "max_context_tokens": 128000,
                "max_output_tokens": 4096,
                "supported_languages": ["en", "es", "fr", "de", "ja", "zh"],
                "cost_per_1k_input": 0.005,
                "cost_per_1k_output": 0.015,
                "typical_latency_ms": 800,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Reasoning", "Threat Analysis", "Recommendation Generation", "Report Writing", "Evidence Explanation"]
            },
            {
                "model_id": "mistral-large",
                "provider": "mistral",
                "display_name": "Mistral Large 2",
                "version": "2407",
                "max_context_tokens": 128000,
                "max_output_tokens": 4096,
                "supported_languages": ["en", "fr", "es", "de", "it"],
                "cost_per_1k_input": 0.002,
                "cost_per_1k_output": 0.006,
                "typical_latency_ms": 500,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Summarization", "Timeline Generation", "Evidence Explanation", "IOC Correlation"]
            },
            {
                "model_id": "deepseek-reasoning",
                "provider": "deepseek",
                "display_name": "DeepSeek R1 Advanced Reasoning",
                "version": "R1-0125",
                "max_context_tokens": 64000,
                "max_output_tokens": 8192,
                "supported_languages": ["en", "zh"],
                "cost_per_1k_input": 0.0015,
                "cost_per_1k_output": 0.004,
                "typical_latency_ms": 1100,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Threat Hunting", "Reasoning", "IOC Correlation", "Risk Assessment"]
            },
            {
                "model_id": "qwen-2.5-72b",
                "provider": "qwen",
                "display_name": "Qwen 2.5 72B Instruct",
                "version": "2.5-72b",
                "max_context_tokens": 128000,
                "max_output_tokens": 4096,
                "supported_languages": ["en", "zh", "ja"],
                "cost_per_1k_input": 0.001,
                "cost_per_1k_output": 0.003,
                "typical_latency_ms": 600,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Summarization", "Report Writing", "Timeline Generation"]
            },
            {
                "model_id": "llama-3.3-70b",
                "provider": "llama",
                "display_name": "Meta Llama 3.3 70B Instruct",
                "version": "3.3",
                "max_context_tokens": 128000,
                "max_output_tokens": 4096,
                "supported_languages": ["en", "es", "de", "fr"],
                "cost_per_1k_input": 0.0008,
                "cost_per_1k_output": 0.002,
                "typical_latency_ms": 450,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Summarization", "Threat Analysis", "Evidence Explanation"]
            },
            {
                "model_id": "ollama-local",
                "provider": "ollama",
                "display_name": "Local Ollama Instance (Zero Data Egress)",
                "version": "local-latest",
                "max_context_tokens": 32000,
                "max_output_tokens": 2048,
                "supported_languages": ["en"],
                "cost_per_1k_input": 0.0,
                "cost_per_1k_output": 0.0,
                "typical_latency_ms": 300,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Summarization", "Threat Hunting", "Evidence Explanation", "IOC Correlation", "Local Enterprise Search"]
            },
            {
                "model_id": "enterprise-self-hosted",
                "provider": "enterprise_local",
                "display_name": "Enterprise Private Security Model (Air-Gapped)",
                "version": "v4.2.0-secure",
                "max_context_tokens": 128000,
                "max_output_tokens": 4096,
                "supported_languages": ["en", "de", "es", "fr"],
                "cost_per_1k_input": 0.0,
                "cost_per_1k_output": 0.0,
                "typical_latency_ms": 400,
                "is_available": True,
                "health_status": ModelHealthStatus.HEALTHY.value,
                "capabilities": ["Summarization", "Threat Analysis", "Report Writing", "Evidence Explanation", "Risk Assessment", "Recommendation Generation", "Threat Hunting", "Timeline Generation", "IOC Correlation", "Future AI Skills"]
            }
        ]
        for item in defaults:
            self.register_model(item["model_id"], item)

    def register_model(self, model_id: str, metadata: Dict[str, Any]):
        self._models[model_id.lower()] = metadata

    def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        return self._models.get(model_id.lower())

    def update_health(self, model_id: str, status: str, latency: int = 0):
        m = self.get_model(model_id)
        if m:
            m["health_status"] = status
            if latency > 0:
                m["typical_latency_ms"] = latency

    def list_all(self) -> List[Dict[str, Any]]:
        return list(self._models.values())

    def filter_by_capability(self, capability: str) -> List[Dict[str, Any]]:
        return [m for m in self._models.values() if capability in m.get("capabilities", []) and m.get("is_available")]


class CapabilityRegistry:
    """
    Capability Registry mapping standardized SOC and threat intelligence skills
    to preferred LLM execution parameters and failover provider ladders.
    """
    def __init__(self):
        self._capabilities: Dict[str, Dict[str, Any]] = {}
        self._seed_capabilities()

    def _seed_capabilities(self):
        caps = {
            "Summarization": {
                "default_model": "gemini-3.1-pro",
                "fallback_models": ["mistral-large", "claude-3-5-sonnet", "ollama-local"],
                "parameters": {"temperature": 0.1, "max_tokens": 2048},
                "description": "Concise condensation of verbose multi-channel logs, emails, and case notes."
            },
            "Threat Analysis": {
                "default_model": "claude-3-5-sonnet",
                "fallback_models": ["gpt-4o", "gemini-3.1-pro", "deepseek-reasoning", "enterprise-self-hosted"],
                "parameters": {"temperature": 0.2, "max_tokens": 4096},
                "description": "Deep cryptographic, behavioural, and infrastructural threat profiling of targeted indicators."
            },
            "Report Writing": {
                "default_model": "gpt-4o",
                "fallback_models": ["claude-3-5-sonnet", "gemini-3.1-pro", "qwen-2.5-72b"],
                "parameters": {"temperature": 0.2, "max_tokens": 8192},
                "description": "Generation of executive and technical formal incident compliance narratives and audit reports."
            },
            "Evidence Explanation": {
                "default_model": "gemini-3.1-pro",
                "fallback_models": ["claude-3-5-sonnet", "llama-3.3-70b", "ollama-local"],
                "parameters": {"temperature": 0.1, "max_tokens": 2048},
                "description": "Plain-language and forensic explanation of obscure DNS records, hex dumps, and header metadata."
            },
            "Risk Assessment": {
                "default_model": "claude-3-5-sonnet",
                "fallback_models": ["gpt-4o", "deepseek-reasoning", "enterprise-self-hosted"],
                "parameters": {"temperature": 0.2, "max_tokens": 3072},
                "description": "Quantitative and qualitative assessment of operational vulnerability, exposure, and financial threat impact."
            },
            "Recommendation Generation": {
                "default_model": "gpt-4o",
                "fallback_models": ["claude-3-5-sonnet", "gemini-3.1-pro", "enterprise-self-hosted"],
                "parameters": {"temperature": 0.3, "max_tokens": 2048},
                "description": "Actionable containment, eradication, sinkhole, and firewall mitigative advice for SOC operations."
            },
            "Threat Hunting": {
                "default_model": "deepseek-reasoning",
                "fallback_models": ["claude-3-5-sonnet", "gpt-4o", "ollama-local"],
                "parameters": {"temperature": 0.2, "max_tokens": 4096},
                "description": "Formulating proactive Sigma rules, YARA rules, Splunk SPL queries, and hypothesis-driven hunt workflows."
            },
            "Timeline Generation": {
                "default_model": "gemini-3.1-pro",
                "fallback_models": ["mistral-large", "qwen-2.5-72b", "gpt-4o"],
                "parameters": {"temperature": 0.1, "max_tokens": 4096},
                "description": "Chronological sequencing and event ordering across heterogeneous forensic artifacts and network logs."
            },
            "IOC Correlation": {
                "default_model": "claude-3-5-sonnet",
                "fallback_models": ["deepseek-reasoning", "gemini-3.1-pro", "ollama-local", "enterprise-self-hosted"],
                "parameters": {"temperature": 0.15, "max_tokens": 3072},
                "description": "Multi-dimensional pivoting across DNS, WHOIS, BGP routing, SSL hashes, and Threat Intel databases."
            },
            "Future AI Skills": {
                "default_model": "gemini-3.1-pro",
                "fallback_models": ["claude-3-5-sonnet", "gpt-4o", "enterprise-self-hosted"],
                "parameters": {"temperature": 0.25, "max_tokens": 4096},
                "description": "Extensible integration point for emergent autonomous investigative skills and specialized fine-tuned models."
            }
        }
        for name, data in caps.items():
            self._capabilities[name.lower()] = {
                "capability_name": name,
                "default_model": data["default_model"],
                "fallback_models": data["fallback_models"],
                "parameters": data["parameters"],
                "description": data["description"]
            }

    def get_capability(self, capability_name: str) -> Optional[Dict[str, Any]]:
        return self._capabilities.get(capability_name.lower())

    def list_capabilities(self) -> List[Dict[str, Any]]:
        return list(self._capabilities.values())

    def add_capability(self, name: str, config: Dict[str, Any]):
        self._capabilities[name.lower()] = config
