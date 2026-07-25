# PHOENIX X: AI Security Brain — Provider & Model Integration Guide

## Onboarding Custom AI Providers
The PHOENIX AI Security Brain utilizes a decoupled architecture where concrete model implementations inherit from the abstract `ProviderInterface` (`app/ai_brain/providers.py`). 

### Implementing a New Provider Adapter
To add support for a custom enterprise proprietary AI platform or local private inference infrastructure, extend `BaseMockableProvider` or directly implement `ProviderInterface`:

```python
from app.ai_brain.providers import BaseMockableProvider

class CustomEnterpriseProvider(BaseMockableProvider):
    def __init__(self, name: str = "custom_provider"):
        super().__init__(name, default_latency=350, cost_per_input=0.0, cost_per_output=0.0)

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.2,
        **kwargs
    ) -> Dict[str, Any]:
        # Pre-execution circuit breaker validation
        self._check_circuit()
        
        try:
            # Execute HTTP POST to proprietary local inference server
            # response = await my_custom_client.post(endpoint="/infer", payload={...})
            result_text = "Analysis complete via custom infrastructure."
            
            return self._simulate_successful_response(prompt, system_prompt, model or "enterprise-v1", max_tokens)
        except Exception as err:
            # Trigger failure recording in failover circuit breaker
            self.circuit_breaker.record_failure()
            raise err
```

## Configuring Provider Hierarchy & Failover
The `ProviderManager` handles failover operations automatically. When invoking AI inferences, specify the fallback cascade hierarchy:

1. **Primary Endpoint**: e.g., `Claude 3.5 Sonnet` (High Reasoning Accuracy)
2. **First Fallback**: e.g., `Google Gemini 3.1 Pro` (High Token Window)
3. **Air-Gapped Ultimate Fallback**: e.g., `Ollama Local` (Zero External Data Egress)

```python
result, failover_logs = await provider_manager.execute_with_failover(
    prompt="Evaluate this Suspicious Domain",
    primary_provider_name="claude",
    model_id="claude-3-5-sonnet",
    fallback_provider_names=["gemini", "openai", "ollama"]
)
```

## Air-Gapped Zero-Egress Ollama Deployment
For highly compliant organizations (government, defense, banking) where data residency mandates forbid external API transmissions, configure the tenant policy to enforce **LOCAL_ONLY** residency routing:

1. Deploy local model weights using Ollama (e.g., `qwen:72b` or `deepseek-r1`).
2. Set the default capability model ID to `ollama-local` in the `CapabilityRegistry`.
3. When `residency_rule="LOCAL_ONLY"` is passed to the `AIOrchestrator`, the Governance Engine will systematically override external routing directives and direct analytical requests exclusively to self-hosted endpoints.
