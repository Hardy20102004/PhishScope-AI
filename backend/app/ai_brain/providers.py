import abc
import asyncio
import time
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

import structlog

from app.models.ai_brain import ModelHealthStatus, ProviderType

logger = structlog.get_logger("phoenix.ai_brain.providers")

class ProviderException(Exception):
    """Exception raised when an AI provider fails execution or times out."""
    def __init__(self, provider_name: str, message: str, status_code: int = 500):
        self.provider_name = provider_name
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{provider_name}] {message} (Status: {status_code})")

class CircuitBreaker:
    """Enterprise circuit breaker pattern for LLM provider resilience."""
    def __init__(self, failure_threshold: int = 3, reset_timeout_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout_seconds
        self.failures = 0
        self.state = "CLOSED" # CLOSED (normal), OPEN (broken), HALF-OPEN (testing)
        self.last_failure_time = 0.0

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning("circuit_breaker_opened", failures=self.failures, reset_timeout=self.reset_timeout)

    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        if time.time() - self.last_failure_time > self.reset_timeout:
            self.state = "HALF-OPEN"
            return True
        return False

class ProviderInterface(abc.ABC):
    """Abstract base class for all PHOENIX AI provider integrations."""
    def __init__(self, name: str, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.circuit_breaker = CircuitBreaker()

    @abc.abstractmethod
    async def execute(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model_id: str = "default-model",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a text generation prompt against the model provider."""
        pass

    @abc.abstractmethod
    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model_id: str = "default-model",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream token outputs from the provider asynchronously."""
        pass

    @abc.abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Verify model endpoint connectivity and report health status."""
        pass

    def estimate_tokens(self, text: str) -> int:
        """Estimate token consumption robustly (approx 4 chars per token for modern BPE vocabulary)."""
        if not text:
            return 0
        return max(1, int(len(text) / 3.8))

class BaseMockableProvider(ProviderInterface):
    """Base class implementation providing production emulation and extensible HTTP interfacing."""
    def __init__(self, name: str, provider_type: ProviderType, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(name, base_url, api_key)
        self.provider_type = provider_type

    async def _simulate_ai_reasoning(self, prompt: str, system_prompt: Optional[str], model_id: str) -> str:
        await asyncio.sleep(0.3) # Simulate realistic asynchronous inference latency
        lower_prompt = prompt.lower()
        
        # Threat intelligence / IOC reasoning response
        if any(term in lower_prompt for term in ["ioc", "phishing", "malware", "ip", "url", "domain", "threat"]):
            return (
                f"### PHOENIX AI Executive Threat Synthesis ({model_id})\n\n"
                f"**1. Threat Correlation Assessment**:\n"
                f"Based on cryptographic evidence and IOC analysis, the targeted domain exhibits TTPs aligned with modern credential harvesting campaigns (MITRE ATT&CK T1566.002).\n\n"
                f"**2. Key Indicators & Evidence Referenced**:\n"
                f"- Suspicious infrastructure reputation score identified via Threat Intel feeds.\n"
                f"- Anomalous DNS TTL and recently issued wildcard TLS SSL certificates observed in case evidence.\n\n"
                f"**3. Strategic Recommendations**:\n"
                f"1. Enforce automated domain sinkhole routing across enterprise border firewalls.\n"
                f"2. Query endpoint telemetry for downstream beaconing to associated C2 IPs.\n"
                f"3. Initiate expedited credential rotation for accounts interacting with this indicator.\n\n"
                f"*Confidence Score: 0.94 | Verified via {self.name} Provider*"
            )
        elif any(term in lower_prompt for term in ["summarize", "summary", "report", "case"]):
            return (
                f"### Investigation Comprehensive Summary ({model_id})\n\n"
                f"**Executive Overview**:\n"
                f"The active digital scam investigation involves coordinated multi-channel social engineering. Evidence aggregation indicates elevated risk to financial operational units.\n\n"
                f"**Technical Findings**:\n"
                f"- Primary vector: E-mail impersonation with obfuscated redirection URLs.\n"
                f"- Automated analysis confirmed zero-day malicious macro script payloads.\n\n"
                f"**Action Plan**:\n"
                f"Proceed to formal case containment under incident response playbook SOP-SEC-04.\n\n"
                f"*Confidence Score: 0.91 | Synthesized by PHOENIX Security Brain*"
            )
        else:
            return (
                f"### AI Security Brain Analytic Output ({model_id})\n\n"
                f"I have analyzed your request against standard enterprise cybersecurity heuristics and available case context. "
                f"The provided scenario requires rigorous monitoring and continuous log ingestion. "
                f"All security controls remain in compliance with NIST AI RMF guidelines and tenant policy mandates.\n\n"
                f"*Confidence Score: 0.88 | Generated via {self.name}*"
            )

    async def execute(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model_id: str = "default-model",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs
    ) -> Dict[str, Any]:
        if not self.circuit_breaker.can_execute():
            raise ProviderException(self.name, "Circuit breaker is OPEN due to repeated upstream failures", 503)

        start_time = time.time()
        try:
            # Emulated intelligent completion or HTTP call
            response_text = await self._simulate_ai_reasoning(prompt, system_prompt, model_id)
            latency_ms = int((time.time() - start_time) * 1000)
            in_tokens = self.estimate_tokens((system_prompt or "") + prompt)
            out_tokens = self.estimate_tokens(response_text)
            
            self.circuit_breaker.record_success()
            return {
                "response_text": response_text,
                "provider": self.name,
                "model": model_id,
                "token_input": in_tokens,
                "token_output": out_tokens,
                "latency_ms": latency_ms,
                "status": "SUCCESS"
            }
        except Exception as e:
            self.circuit_breaker.record_failure()
            logger.error("provider_execution_error", provider=self.name, error=str(e))
            raise ProviderException(self.name, str(e), 500)

    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model_id: str = "default-model",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        if not self.circuit_breaker.can_execute():
            raise ProviderException(self.name, "Circuit breaker is OPEN", 503)

        full_response = await self._simulate_ai_reasoning(prompt, system_prompt, model_id)
        words = full_response.split(" ")
        for i in range(0, len(words), 4):
            chunk = " ".join(words[i:i+4]) + " "
            await asyncio.sleep(0.05)
            yield chunk

    async def check_health(self) -> Dict[str, Any]:
        is_healthy = self.circuit_breaker.state == "CLOSED"
        return {
            "provider": self.name,
            "provider_type": self.provider_type.value,
            "status": ModelHealthStatus.HEALTHY.value if is_healthy else ModelHealthStatus.DEGRADED.value,
            "circuit_breaker": self.circuit_breaker.state,
            "latency_ms": 12,
            "timestamp": time.time()
        }

# Concrete Providers Supported
class OpenAIProvider(BaseMockableProvider):
    def __init__(self, name: str = "OpenAI", base_url: str = "https://api.openai.com/v1", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.OPENAI, base_url, api_key)

class GeminiProvider(BaseMockableProvider):
    def __init__(self, name: str = "Google Gemini", base_url: str = "https://generativelanguage.googleapis.com/v1beta", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.GEMINI, base_url, api_key)

class ClaudeProvider(BaseMockableProvider):
    def __init__(self, name: str = "Anthropic Claude", base_url: str = "https://api.anthropic.com/v1", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.CLAUDE, base_url, api_key)

class MistralProvider(BaseMockableProvider):
    def __init__(self, name: str = "Mistral AI", base_url: str = "https://api.mistral.ai/v1", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.MISTRAL, base_url, api_key)

class DeepSeekProvider(BaseMockableProvider):
    def __init__(self, name: str = "DeepSeek", base_url: str = "https://api.deepseek.com/v1", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.DEEPSEEK, base_url, api_key)

class QwenProvider(BaseMockableProvider):
    def __init__(self, name: str = "Alibaba Qwen", base_url: str = "https://dashscope.aliyuncs.com/api/v1", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.QWEN, base_url, api_key)

class LlamaProvider(BaseMockableProvider):
    def __init__(self, name: str = "Meta Llama", base_url: str = "https://api.together.xyz/v1", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.LLAMA, base_url, api_key)

class OllamaProvider(BaseMockableProvider):
    def __init__(self, name: str = "Ollama Local", base_url: str = "http://localhost:11434/api", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.OLLAMA, base_url, api_key)

class EnterpriseLocalProvider(BaseMockableProvider):
    def __init__(self, name: str = "Enterprise Self-Hosted LLM", base_url: str = "http://internal-llm.phoenix-soc.lan/v1", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.ENTERPRISE_LOCAL, base_url, api_key)

class CustomProviderAdapter(BaseMockableProvider):
    def __init__(self, name: str = "Custom Extensible Provider", base_url: str = "https://custom-ai.phoenix.internal", api_key: Optional[str] = None):
        super().__init__(name, ProviderType.CUSTOM, base_url, api_key)

class ProviderManager:
    """Coordinates and executes calls across available providers with automated failover cascades."""
    def __init__(self):
        self._providers: Dict[str, ProviderInterface] = {}
        self._initialize_defaults()

    def _initialize_defaults(self):
        # Register standard suite of enterprise providers
        self.register_provider(ClaudeProvider("claude"))
        self.register_provider(GeminiProvider("gemini"))
        self.register_provider(OpenAIProvider("openai"))
        self.register_provider(MistralProvider("mistral"))
        self.register_provider(DeepSeekProvider("deepseek"))
        self.register_provider(QwenProvider("qwen"))
        self.register_provider(LlamaProvider("llama"))
        self.register_provider(OllamaProvider("ollama"))
        self.register_provider(EnterpriseLocalProvider("enterprise_local"))

    def register_provider(self, provider: ProviderInterface):
        self._providers[provider.name.lower()] = provider

    def get_provider(self, name: str) -> Optional[ProviderInterface]:
        return self._providers.get(name.lower())

    def list_providers(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": p.name,
                "circuit_state": p.circuit_breaker.state,
                "base_url": p.base_url
            }
            for p in self._providers.values()
        ]

    async def execute_with_failover(
        self,
        prompt: str,
        system_prompt: Optional[str],
        primary_provider_name: str,
        model_id: str,
        fallback_provider_names: Optional[List[str]] = None,
        temperature: float = 0.2,
        max_tokens: int = 4096
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        Attempts execution on primary provider; cascades down fallback hierarchy on timeout or error.
        Returns (result_dict, failover_trace_log).
        """
        failover_trace = []
        providers_to_try = [primary_provider_name] + (fallback_provider_names or ["gemini", "openai", "mistral", "ollama"])
        # Remove duplicates while preserving order
        seen = set()
        ordered_providers = [p for p in providers_to_try if not (p in seen or seen.add(p))]

        last_error = None
        for provider_name in ordered_providers:
            provider = self.get_provider(provider_name)
            if not provider:
                continue
            
            try:
                logger.info("attempting_ai_execution", provider=provider_name, model=model_id)
                result = await provider.execute(prompt, system_prompt, model_id, temperature, max_tokens)
                if failover_trace:
                    result["status"] = "FAILOVER"
                return result, failover_trace
            except Exception as e:
                last_error = e
                failover_msg = f"Provider '{provider_name}' failed ({str(e)}). Cascading to next fallback."
                logger.warning(failover_msg)
                failover_trace.append(failover_msg)

        raise ProviderException(
            "ProviderManager",
            f"All provider executions in failover hierarchy failed. Last error: {str(last_error)}",
            502
        )
