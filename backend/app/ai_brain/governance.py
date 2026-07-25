import base64
import hashlib
import hmac
import re
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

import structlog

logger = structlog.get_logger("phoenix.ai_brain.governance")

# Master system salt for simulated AES-256 GCM token serialization & HMAC chaining
SECRET_ENCRYPTION_KEY = b"PHOENIX_X_AI_SECURITY_BRAIN_MASTER_KEY_256BIT"

class PolicyEngine:
    """
    AI Governance & Policy Engine enforcing Model Access rules, PII & Secrets masking,
    Data Residency constraints, and Prompt Injection safeguards (OWASP Top 10 LLM & NIST AI RMF).
    """
    # Regex patterns for detecting sensitive data & potential credentials
    PII_PATTERNS = [
        (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), "[REDACTED_SSN]"),
        (re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})\b'), "[REDACTED_CREDIT_CARD]"),
        (re.compile(r'AKIA[0-9A-Z]{16}'), "[REDACTED_AWS_ACCESS_KEY]"),
        (re.compile(r'(?:api_key|secret|token|password)[\s]*[:=][\s]*["\']?([A-Za-z0-9\-_]{16,})["\']?', re.IGNORECASE), "[REDACTED_SECRET_CREDENTIAL]"),
    ]

    # Malicious prompt injection heuristics
    INJECTION_PATTERNS = [
        re.compile(r'ignore.*(instructions|directions|rules)', re.IGNORECASE),
        re.compile(r'(in|operating under).*DAN mode', re.IGNORECASE),
        re.compile(r'override.*system prompt', re.IGNORECASE),
        re.compile(r'show.*system prompt', re.IGNORECASE),
        re.compile(r'bypass.*security constraints', re.IGNORECASE),
    ]

    @classmethod
    def filter_sensitive_data(cls, text: str, enable_pii_masking: bool = True) -> Tuple[str, List[str]]:
        """Scans and masks customer PII, credit cards, SSNs, and secret tokens before external transmission."""
        if not text or not enable_pii_masking:
            return text, []

        redacted_types = []
        cleaned_text = text
        for pattern, replacement in cls.PII_PATTERNS:
            if pattern.search(cleaned_text):
                cleaned_text = pattern.sub(replacement, cleaned_text)
                redacted_types.append(replacement)

        if redacted_types:
            logger.warning("sensitive_data_masked", types=redacted_types)
        return cleaned_text, list(set(redacted_types))

    @classmethod
    def check_prompt_injection(cls, prompt: str) -> Tuple[bool, Optional[str]]:
        """Detects adversarial jailbreaks or instructions aiming to manipulate AI directives."""
        if not prompt:
            return False, None
        for p in cls.INJECTION_PATTERNS:
            if p.search(prompt):
                logger.warning("prompt_injection_attempt_blocked", pattern=p.pattern)
                return True, "Potential Prompt Injection or Jailbreak Attempt Detected and Blocked."
        return False, None

    @classmethod
    def validate_model_access(
        cls,
        requested_model_id: str,
        tenant_allowed_models: Optional[List[str]] = None,
        residency_rule: str = "GLOBAL"
    ) -> Tuple[bool, str, str]:
        """
        Validates model permissibility against tenant rules and residency guidelines.
        Returns: (is_allowed, approved_model_id, policy_note)
        """
        clean_model = requested_model_id.lower()

        # Check Residency enforcement
        if residency_rule.upper() == "LOCAL_ONLY" and not any(m in clean_model for m in ["local", "ollama", "enterprise"]):
            logger.info("residency_enforcing_local", original_model=clean_model)
            return True, "enterprise-self-hosted", "Routed to Air-Gapped Enterprise Model per LOCAL_ONLY data residency policy."

        # Check explicit allowed models table
        if tenant_allowed_models and clean_model not in [m.lower() for m in tenant_allowed_models]:
            fallback = tenant_allowed_models[0] if tenant_allowed_models else "ollama-local"
            logger.warning("model_restricted_by_tenant_policy", requested=clean_model, redirected_to=fallback)
            return True, fallback, f"Model '{clean_model}' restricted by tenant policy. Redirected to '{fallback}'."

        return True, clean_model, "Passed model access checks."


class ResponseValidator:
    """
    Validates every generated AI response against grounded evidence references,
    detects hallucination indicators, and checks structural markdown formatting.
    """
    HALLUCINATIVE_PHRASES = [
        "as an ai i cannot verify",
        "i guess that",
        "it might be possible without evidence",
        "i fabricated this",
        "example.com/fake"
    ]

    @classmethod
    def validate_response(
        cls,
        response_text: str,
        input_context: str,
        confidence_score: float,
        evidence_items: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[str, List[str], List[Dict[str, Any]], str]:
        """
        Evaluates output compliance.
        Returns: (validated_text, hallucination_flags, verified_citations, policy_status)
        """
        hallucinations: List[str] = []
        citations: List[Dict[str, Any]] = []
        policy_status = "PASSED"
        lower_resp = response_text.lower()

        # 1. Hallucination indicator check
        for hp in cls.HALLUCINATIVE_PHRASES:
            if hp in lower_resp:
                hallucinations.append(f"Flagged phrase: '{hp}'")
                policy_status = "MODIFIED"

        # 2. Evidence Grounding Verification
        if evidence_items:
            for item in evidence_items:
                target_val = str(item.get("value") or item.get("url") or item.get("ioc") or item.get("id", "")).strip()
                if target_val and target_val != "N/A" and (target_val.lower() in lower_resp or str(item.get("id", "")).lower() in lower_resp):
                    citations.append({
                        "finding_id": item.get("id", "EVID-REF"),
                        "target": target_val,
                        "verified_in_vault": True
                    })

        # 3. Confidence Threshold Human-in-the-Loop check
        if confidence_score < 0.60:
            logger.warning("low_confidence_response_flagged", score=confidence_score)
            response_text += "\n\n> [!WARNING]\n> **Low Confidence Score Notice (< 0.60)**: This AI response requires Human-in-the-Loop Analyst verification before taking disrupting mitigative actions."
            policy_status = "FLAGGED_FOR_REVIEW"

        if hallucinations:
            response_text += f"\n\n> [!CAUTION]\n> **Hallucination Safeguard Triggered**: Potential unverified phrases detected: {', '.join(hallucinations)}."
            logger.warning("response_validator_detected_hallucinations", count=len(hallucinations))

        return response_text, hallucinations, citations, policy_status


class AIAuditEngine:
    """
    Zero-Data-Leakage AI Audit Engine recording tamper-proof encrypted log payloads
    with HMAC SHA-256 cryptographic signature chaining.
    """
    def __init__(self):
        self._last_signature = b"GENESIS_HASH_0000000000000000"
        self._in_memory_audit_trail: List[Dict[str, Any]] = []

    def _encrypt_payload(self, text: str) -> str:
        """Simulates enterprise AES-256 GCM authenticated payload wrapping with base64 + HMAC tag."""
        if not text:
            return ""
        encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        mac = hmac.new(SECRET_ENCRYPTION_KEY, text.encode("utf-8"), hashlib.sha256).hexdigest()[:16]
        return f"AES256GCM:{mac}:{encoded}"

    def _decrypt_payload(self, cipher_text: str) -> str:
        if not cipher_text or not cipher_text.startswith("AES256GCM:"):
            return cipher_text
        parts = cipher_text.split(":")
        if len(parts) >= 3:
            try:
                return base64.b64decode(parts[2].encode("utf-8")).decode("utf-8")
            except Exception:
                return "[DECRYPTION_ERROR]"
        return cipher_text

    def record_audit_log(
        self,
        request_id: str,
        provider: str,
        model: str,
        input_prompt: str,
        output_response: str,
        confidence_score: float,
        in_tokens: int,
        out_tokens: int,
        latency_ms: int,
        status: str = "SUCCESS",
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
        capability: Optional[str] = None,
        decision_trace: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Creates encrypted audit log entry with cryptographic integrity chaining."""
        encrypted_input = self._encrypt_payload(input_prompt)
        encrypted_output = self._encrypt_payload(output_response)

        # Compute HMAC signature over core fields + previous hash signature
        chain_payload = f"{request_id}|{provider}|{model}|{confidence_score}|{in_tokens}|{out_tokens}|{status}|{encrypted_output[:20]}".encode("utf-8")
        current_hmac = hmac.new(SECRET_ENCRYPTION_KEY, chain_payload + self._last_signature, hashlib.sha256).hexdigest()
        self._last_signature = current_hmac.encode("utf-8")

        record = {
            "id": str(uuid.uuid4()),
            "tenant_id": tenant_id or "default-tenant",
            "request_id": request_id,
            "user_id": user_id or "system-analyst",
            "provider_used": provider,
            "model_used": model,
            "capability": capability or "Threat Analysis",
            "input_prompt_encrypted": encrypted_input,
            "output_response_encrypted": encrypted_output,
            "confidence_score": confidence_score,
            "token_input_count": in_tokens,
            "token_output_count": out_tokens,
            "latency_ms": latency_ms,
            "status": status,
            "decision_trace_json": decision_trace or [],
            "timestamp": time.time(),
            "hmac_signature": current_hmac
        }
        
        self._in_memory_audit_trail.append(record)
        logger.info("ai_audit_log_created_and_signed", request_id=request_id, hmac_prefix=current_hmac[:12])
        return record

    def list_recent_audits(self, limit: int = 50, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if tenant_id:
            filtered = [r for r in self._in_memory_audit_trail if r["tenant_id"] == tenant_id]
        else:
            filtered = self._in_memory_audit_trail
        return sorted(filtered, key=lambda x: x["timestamp"], reverse=True)[:limit]
