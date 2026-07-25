import hashlib
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import structlog

logger = structlog.get_logger("phoenix.ai_brain.optimization")

class RateLimiter:
    """Sliding-window token and request rate limiter per tenant and user."""
    def __init__(self, requests_per_minute: int = 60, tokens_per_minute: int = 100000):
        self.rpm_limit = requests_per_minute
        self.tpm_limit = tokens_per_minute
        # Structure: key -> {"reset_time": timestamp, "requests": count, "tokens": count}
        self.usage_buckets: Dict[str, Dict[str, Union[int, float]]] = {}

    def is_allowed(self, identity_key: str, estimated_tokens: int = 0) -> Tuple[bool, str]:
        current_time = time.time()
        if identity_key not in self.usage_buckets or current_time >= self.usage_buckets[identity_key]["reset_time"]:
            self.usage_buckets[identity_key] = {
                "reset_time": current_time + 60.0,
                "requests": 1,
                "tokens": estimated_tokens
            }
            return True, "Allowed"

        bucket = self.usage_buckets[identity_key]
        if bucket["requests"] >= self.rpm_limit:
            return False, f"Rate limit exceeded: Max {self.rpm_limit} requests per minute."
        if bucket["tokens"] + estimated_tokens >= self.tpm_limit:
            return False, f"Token rate limit exceeded: Max {self.tpm_limit} tokens per minute."

        bucket["requests"] += 1
        bucket["tokens"] += estimated_tokens
        return True, "Allowed"

class PromptCache:
    """High-performance semantically hashed prompt caching wrapper."""
    def __init__(self, ttl_seconds: int = 3600, max_entries: int = 1000):
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        # Structure: hash -> (timestamp, response_dict)
        self._cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}

    def _generate_key(self, prompt: str, system_prompt: Optional[str], model_id: str) -> str:
        payload = f"{model_id}|{system_prompt or ''}|{prompt.strip().lower()}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get(self, prompt: str, system_prompt: Optional[str], model_id: str) -> Optional[Dict[str, Any]]:
        key = self._generate_key(prompt, system_prompt, model_id)
        if key in self._cache:
            timestamp, data = self._cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                logger.info("prompt_cache_hit", key=key[:10], model=model_id)
                data_copy = dict(data)
                data_copy["cached"] = True
                return data_copy
            else:
                del self._cache[key]
        return None

    def set(self, prompt: str, system_prompt: Optional[str], model_id: str, data: Dict[str, Any]):
        if len(self._cache) >= self.max_entries:
            # Remove oldest 10% of entries (LRU-like trimming)
            sorted_keys = sorted(self._cache.keys(), key=lambda k: self._cache[k][0])
            for k in sorted_keys[:int(self.max_entries * 0.1)]:
                del self._cache[k]
        
        key = self._generate_key(prompt, system_prompt, model_id)
        self._cache[key] = (time.time(), data)

class ContextCompressor:
    """Intelligent context compression algorithms to prevent token saturation."""
    @staticmethod
    def compress_by_truncation(context_text: str, max_characters: int = 16000) -> str:
        """Retains recent logs and critical summary headers while pruning redundant interior noise."""
        if len(context_text) <= max_characters:
            return context_text
        
        half = int((max_characters - 500) / 2)
        head = context_text[:half]
        tail = context_text[-half:]
        return f"{head}\n\n[... PHOENIX CONTEXT COMPRESSOR: Pruned {len(context_text) - max_characters} interior characters for token optimization ...]\n\n{tail}"

    @staticmethod
    def deduplicate_evidence_lines(evidence_list: List[str]) -> List[str]:
        """Removes duplicated indicators, logs, or repeating timestamps."""
        seen = set()
        deduped = []
        for line in evidence_list:
            clean = line.strip()
            if clean and clean not in seen:
                seen.add(clean)
                deduped.append(line)
        return deduped

class TokenManager:
    """Enterprise token management, quota budgets, and live cost calculation."""
    # Pricing table per 1000 tokens (Input, Output) in USD
    MODEL_PRICING: Dict[str, Tuple[float, float]] = {
        "gpt-4o": (0.005, 0.015),
        "gemini-3.1-pro": (0.0035, 0.0105),
        "claude-3-5-sonnet": (0.003, 0.015),
        "mistral-large": (0.002, 0.006),
        "deepseek-reasoning": (0.0015, 0.004),
        "qwen-2.5-72b": (0.001, 0.003),
        "llama-3.3-70b": (0.0008, 0.002),
        "ollama-local": (0.0, 0.0),
        "enterprise_local": (0.0, 0.0),
    }

    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.prompt_cache = PromptCache()

    def calculate_cost(self, model_id: str, input_tokens: int, output_tokens: int) -> float:
        input_price, output_price = 0.003, 0.015 # Default conservative rate
        for key, rates in self.MODEL_PRICING.items():
            if key in model_id.lower():
                input_price, output_price = rates
                break
        
        cost_in = (input_tokens / 1000.0) * input_price
        cost_out = (output_tokens / 1000.0) * output_price
        return round(cost_in + cost_out, 6)

    def optimize_and_validate(self, tenant_id: str, prompt: str, system_prompt: Optional[str], model_id: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Performs rate limit check and cache validation.
        Returns: (is_allowed, reason_or_status, cached_result_if_found)
        """
        estimated_tokens = int((len(prompt) + len(system_prompt or "")) / 3.8)
        allowed, reason = self.rate_limiter.is_allowed(f"tenant_{tenant_id}", estimated_tokens)
        if not allowed:
            return False, reason, None

        cached = self.prompt_cache.get(prompt, system_prompt, model_id)
        if cached:
            return True, "Cache hit", cached

        return True, "Allowed", None

    def record_usage(self, tenant_id: str, model_id: str, in_tokens: int, out_tokens: int) -> Dict[str, Any]:
        cost = self.calculate_cost(model_id, in_tokens, out_tokens)
        logger.info("token_consumption_recorded", tenant_id=tenant_id, model=model_id, in_tokens=in_tokens, out_tokens=out_tokens, cost_usd=cost)
        return {
            "model": model_id,
            "input_tokens": in_tokens,
            "output_tokens": out_tokens,
            "cost_usd": cost,
            "timestamp": time.time()
        }
