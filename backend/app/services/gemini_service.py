"""
gemini_service.py
-----------------
Centralized Google Gemini AI Client for PhishScope-AI / PHOENIX Backend.
Uses the new google.genai SDK (replaces deprecated google.generativeai).

Supports ALL Gemini model versions with automatic fallback:
  - gemini-2.5-pro    (Best reasoning, primary for deep analysis)
  - gemini-2.5-flash  (Fast, good for quick triage)
  - gemini-2.0-flash  (Balanced speed/quality)
  - gemini-1.5-pro    (Stable, high quality)
  - gemini-1.5-flash  (Fast legacy fallback)

Designed for UP Police Cyber Cell — PhishScope-AI Phishing Investigation Platform.
"""
import asyncio
import json
import logging
import re
from typing import Any, Dict, List, Optional

from google import genai
from google.genai import types

from app.core.config import settings

logger = logging.getLogger(__name__)

# ============================================================
# System Prompt — UP Police Cyber Cell Context
# ============================================================
PHISHSCOPE_SYSTEM_PROMPT = """You are PhishScope-AI, an advanced Phishing & Cyber Threat Investigation Engine 
developed for the UP Police Cyber Cell, Uttar Pradesh, India. 

Your role is to analyze URLs, domains, and web infrastructure data to detect phishing, fraud, and cyber scams.
You must provide:
1. Clear threat assessment in plain language that a police officer can understand
2. Evidence-backed reasoning (not speculation)
3. Specific indicators of compromise (IOCs)
4. Actionable recommendations for the Cyber Cell team

Always respond in structured JSON format as instructed. Be precise, factual, and concise.
Prioritize detection of:
- Banking fraud (SBI, HDFC, Paytm, PhonePe impersonation)  
- Government site spoofing (.gov.in, NIC portals)
- UPI scams and fake payment gateways
- OTP/credential harvesting pages
- Job fraud and loan scam sites common in UP region
"""


class GeminiService:
    """
    Production-grade Gemini AI service with multi-model fallback.
    Uses google.genai (new SDK, replaces deprecated google.generativeai).
    
    Usage:
        service = GeminiService()
        result = await service.analyze_phishing_threat(url, evidence)
    """
    
    ALL_MODELS = [
        "gemini-2.5-pro",
        "gemini-2.5-flash", 
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
    ]
    
    def __init__(self):
        self._configured = False
        self._client: Optional[genai.Client] = None
        self._active_model_name: Optional[str] = None
        
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. AI analysis will use fallback templates.")
            return
        
        try:
            self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self._configured = True
            self._active_model_name = settings.GEMINI_PRIMARY_MODEL
            logger.info(f"GeminiService initialized (google.genai SDK) | primary model: {self._active_model_name}")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
    
    def _get_generate_config(self) -> types.GenerateContentConfig:
        """Returns generation config tuned for security analysis."""
        return types.GenerateContentConfig(
            temperature=settings.GEMINI_TEMPERATURE,
            max_output_tokens=settings.GEMINI_MAX_OUTPUT_TOKENS,
            response_mime_type="application/json",
            system_instruction=PHISHSCOPE_SYSTEM_PROMPT,
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_MEDIUM_AND_ABOVE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_NONE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_NONE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_NONE"
                ),
            ],
        )
    
    def _get_fallback_models(self) -> List[str]:
        """Returns ordered list of models to try: primary, fast, then fallbacks."""
        models = [settings.GEMINI_PRIMARY_MODEL, settings.GEMINI_FAST_MODEL]
        for m in settings.gemini_fallback_model_list:
            if m not in models:
                models.append(m)
        return models
    
    async def _generate_with_fallback(self, prompt: str) -> Optional[str]:
        """
        Tries models in priority order until one succeeds.
        Returns the raw text response or None if all fail.
        """
        if not self._configured or not self._client:
            return None
        
        config = self._get_generate_config()
        models_to_try = self._get_fallback_models()
        last_error = None
        
        for model_name in models_to_try:
            try:
                logger.info(f"Attempting Gemini generation with model: {model_name}")
                
                # Run sync Gemini call in thread pool to not block async event loop
                response = await asyncio.to_thread(
                    self._client.models.generate_content,
                    model=model_name,
                    contents=prompt,
                    config=config,
                )
                
                if response.text:
                    self._active_model_name = model_name
                    logger.info(f"✅ Gemini generation successful | model: {model_name}")
                    return response.text
                    
            except Exception as e:
                last_error = e
                logger.warning(f"Model {model_name} failed: {type(e).__name__}: {e}. Trying next...")
                continue
        
        logger.error(f"All Gemini models failed. Last error: {last_error}")
        return None
    
    async def analyze_phishing_threat(
        self,
        url: str,
        intel_data: Dict[str, Any],
        brand_data: Dict[str, Any],
        infra_data: Dict[str, Any],
        risk_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Main phishing analysis — sends all investigation evidence to Gemini
        and gets a structured threat narrative back.
        """
        prompt = self._build_phishing_analysis_prompt(url, intel_data, brand_data, infra_data, risk_data)
        raw_response = await self._generate_with_fallback(prompt)
        
        if raw_response:
            return self._parse_gemini_response(raw_response, url, risk_data)
        else:
            return self._build_fallback_analysis(url, intel_data, brand_data, infra_data, risk_data)
    
    async def quick_classify(self, url: str) -> Dict[str, Any]:
        """
        Fast URL classification using the flash model.
        Returns a simple phishing/safe verdict with confidence.
        """
        prompt = f"""Classify this URL for phishing risk. 
URL: {url}

Respond with JSON:
{{
  "verdict": "PHISHING",
  "confidence": 85,
  "reason": "one sentence explanation",
  "ioc_type": "typosquatting"
}}

verdict options: PHISHING, SUSPICIOUS, SAFE, UNKNOWN
ioc_type options: typosquatting, credential_harvesting, brand_impersonation, malware_distribution, clean, unknown"""
        
        if self._configured and self._client:
            try:
                config = types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=256,
                    response_mime_type="application/json",
                    system_instruction=PHISHSCOPE_SYSTEM_PROMPT,
                )
                response = await asyncio.to_thread(
                    self._client.models.generate_content,
                    model=settings.GEMINI_FAST_MODEL,
                    contents=prompt,
                    config=config,
                )
                if response.text:
                    clean = re.sub(r'```(?:json)?', '', response.text).strip()
                    return json.loads(clean)
            except Exception as e:
                logger.warning(f"Quick classify failed: {e}")
        
        return {
            "verdict": "UNKNOWN",
            "confidence": 0,
            "reason": "AI classification unavailable",
            "ioc_type": "unknown"
        }
    
    async def analyze_page_content(self, url: str, page_text: str) -> Dict[str, Any]:
        """
        Analyzes scraped webpage content for phishing indicators.
        Useful for detecting fake login forms, urgency language, brand impersonation.
        """
        truncated_content = page_text[:3000] if len(page_text) > 3000 else page_text
        
        prompt = f"""Analyze this webpage content for phishing indicators.
URL: {url}

Page Content:
---
{truncated_content}
---

Look for: fake login forms, urgency language, brand impersonation, suspicious form targets, OTP/UPI harvesting.

Respond with JSON:
{{
  "contains_login_form": false,
  "urgency_language_detected": false,
  "brand_impersonation": false,
  "impersonated_brand": null,
  "suspicious_form_actions": false,
  "otp_harvesting_indicators": false,
  "phishing_confidence": 0,
  "key_indicators": [],
  "gemini_verdict": "LIKELY_SAFE",
  "analyst_note": "explanation for UP Police Cyber Cell report"
}}"""
        
        raw = await self._generate_with_fallback(prompt)
        if raw:
            try:
                clean = re.sub(r'```(?:json)?', '', raw).strip()
                return json.loads(clean)
            except json.JSONDecodeError:
                pass
        return {
            "phishing_confidence": 0,
            "gemini_verdict": "UNKNOWN",
            "analyst_note": "Page content analysis unavailable"
        }
    
    def _build_phishing_analysis_prompt(
        self,
        url: str,
        intel: Dict,
        brand: Dict,
        infra: Dict,
        risk: Dict,
    ) -> str:
        """Builds a structured evidence prompt for Gemini phishing analysis."""
        certs = infra.get("certificates", [])
        if not certs:
            cert_info = "No TLS certificate found"
        else:
            c = certs[0]
            cert_info = (
                f"Issuer: {c.get('issuer', 'Unknown')}, "
                f"Valid: {c.get('is_valid', False)}, "
                f"TLS Version: {c.get('tls_version', 'Unknown')}, "
                f"Expires: {c.get('valid_to', 'Unknown')}"
            )
        
        return f"""Analyze this URL for phishing threats based on evidence collected by PhishScope-AI.

## URL Under Investigation
{url}

## URL Intelligence Evidence
- URL Length: {intel.get('url_length', 0)} characters (>100 is suspicious)
- Entropy Score: {intel.get('entropy', 0):.2f}/6.0 (>4.5 indicates obfuscation/randomization)
- Suspicious Keywords Found: {intel.get('suspicious_keywords_found', [])}
- Credential Pattern (user:pass@domain): {intel.get('credential_pattern', False)}
- Nested Redirect Parameters: {intel.get('nested_redirect_parameters', [])}

## Brand Impersonation Analysis
- Typosquatting Detected: {brand.get('is_typosquat', False)}
- Targeted Brand: {brand.get('typosquat_target', 'None')}
- Homograph Attack (Unicode deception): {brand.get('is_homograph', False)}
- Brand Impersonation Confidence: {brand.get('brand_impersonation_score', 0.0):.0%}

## Infrastructure Evidence
- Resolved IP Addresses: {infra.get('ips', [])}
- Nameservers: {infra.get('nameservers', [])}
- MX Records (email infrastructure): {infra.get('mx_records', [])}
- TLS Certificate: {cert_info}
- SPF/DMARC (TXT Records): {infra.get('txt_records', [])}

## Pre-computed Risk Scores
- Overall Risk Score: {risk.get('overall_risk_score', 0)}/100
- Threat Severity: {risk.get('threat_severity', 'UNKNOWN')}
- URL Risk Score: {risk.get('url_risk', 0)}/70
- Brand Risk Score: {risk.get('brand_risk', 0)}/80
- Infrastructure Risk Score: {risk.get('infrastructure_risk', 0)}/40
- Evidence Quality: {risk.get('evidence_quality', 'UNKNOWN')}

## Task
Provide comprehensive phishing threat analysis for UP Police Cyber Cell.
Respond ONLY with this exact JSON (no markdown, no extra text):
{{
  "risk_narrative": "2-3 sentences explaining WHY this URL is dangerous or safe. Write for a police officer, not a technical expert. Be specific about what criminal activity this enables.",
  "threat_summary": "Comma-separated list of active threat types OR 'Clean'",
  "recommended_next_steps": "Specific police action: block/monitor/FIR/close investigation",
  "evidence_correlation": "How do the DNS, TLS, URL, and brand evidence connect?",
  "iocs": ["specific", "indicators", "of", "compromise"],
  "confidence_adjusted_severity": "LOW",
  "gemini_risk_score": 0,
  "model_used": "auto",
  "report_summary_hindi": "एक वाक्य हिंदी में"
}}"""
    
    def _parse_gemini_response(self, raw_text: str, url: str, risk_data: Dict) -> Dict[str, Any]:
        """Safely parses Gemini JSON response with error recovery."""
        try:
            clean = re.sub(r'```(?:json)?', '', raw_text).strip()
            # Also strip trailing ``` if present
            clean = clean.rstrip('`').strip()
            result = json.loads(clean)
            result["model_used"] = self._active_model_name or "unknown"
            result["ai_provider"] = "Google Gemini"
            return result
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Gemini JSON: {e}. Raw: {raw_text[:300]}")
            return {
                "risk_narrative": raw_text[:800],
                "threat_summary": "AI analysis partially available — see narrative",
                "recommended_next_steps": "Manual review recommended",
                "evidence_correlation": "JSON parsing failed — raw text returned as narrative",
                "iocs": [],
                "confidence_adjusted_severity": risk_data.get("threat_severity", "UNKNOWN"),
                "gemini_risk_score": risk_data.get("overall_risk_score", 0),
                "model_used": self._active_model_name or "unknown",
                "ai_provider": "Google Gemini (partial)",
                "report_summary_hindi": "विश्लेषण आंशिक रूप से उपलब्ध है",
            }
    
    def _build_fallback_analysis(
        self,
        url: str,
        intel: Dict,
        brand: Dict,
        infra: Dict,
        risk: Dict,
    ) -> Dict[str, Any]:
        """Rule-based fallback when Gemini API is unavailable."""
        severity = risk.get("threat_severity", "LOW")
        score = risk.get("overall_risk_score", 0)
        threats = []
        narrative_parts = [f"Investigation of {url} indicates a {severity} threat (Score: {score}/100). "]
        
        if brand.get("is_typosquat"):
            target = brand.get("typosquat_target", "a known brand")
            narrative_parts.append(f"The domain is typosquatting '{target}' — a common phishing technique where criminals use a misspelled version of a trusted brand name to deceive victims. ")
            threats.append(f"Typosquatting ({target})")
        
        if brand.get("is_homograph"):
            narrative_parts.append("A homograph attack was detected — the domain uses Unicode characters that look like standard letters to create a deceptive domain name. ")
            threats.append("Homograph Attack")
            
        if intel.get("credential_pattern"):
            narrative_parts.append("Embedded credential pattern found in URL (user:password@domain format). This is used to bypass URL scanners and deceive victims. ")
            threats.append("Credential Embedding")
            
        if intel.get("suspicious_keywords_found"):
            kw = ", ".join(intel.get("suspicious_keywords_found"))
            narrative_parts.append(f"Phishing keywords found: {kw}. ")
            threats.append(f"Phishing Keywords ({kw})")
        
        certs = infra.get("certificates", [])
        if not certs:
            narrative_parts.append("No valid TLS certificate — this site cannot provide secure communication. ")
            threats.append("Missing TLS Certificate")
        
        if score < 30 and not threats:
            narrative_parts.append("No significant malicious indicators were found. The URL appears legitimate.")
            threats.append("Clean")
        
        actions = {
            "CRITICAL": "Immediately block this domain at the firewall/DNS level. If a citizen has already accessed it, preserve digital evidence (screenshots, network logs). File FIR under IT Act Section 66C/66D if victim complaint received.",
            "HIGH": "Block access to this domain. Warn users who may have visited. Monitor for related domains. Escalate to Cyber Cell supervisor.",
            "MEDIUM": "Monitor traffic to this domain. Issue advisory to potential victims. Watch for phishing complaint patterns.",
            "LOW": "No immediate action required. Continue standard threat monitoring.",
        }
        
        hindi_map = {
            "CRITICAL": "यह URL अत्यंत खतरनाक है — साइबर धोखाधड़ी का संदेह, तुरंत ब्लॉक करें।",
            "HIGH": "यह URL संदिग्ध है और फ़िशिंग के संकेत हैं — Cyber Cell को तुरंत सूचित करें।",
            "MEDIUM": "यह URL संभावित रूप से खतरनाक है — निगरानी और जांच आवश्यक है।",
            "LOW": "यह URL अपेक्षाकृत सुरक्षित प्रतीत होता है — नियमित निगरानी जारी रखें।",
        }
        
        return {
            "risk_narrative": "".join(narrative_parts),
            "threat_summary": ", ".join(threats) if threats else "Clean",
            "recommended_next_steps": actions.get(severity, actions["LOW"]),
            "evidence_correlation": "Analysis based on DNS infrastructure, TLS certificate status, URL structural analysis, and brand similarity algorithms. (Gemini AI unavailable — using rule-based fallback engine)",
            "iocs": [url] + infra.get("ips", []),
            "confidence_adjusted_severity": severity,
            "gemini_risk_score": score,
            "model_used": "rule_based_fallback",
            "ai_provider": "PhishScope Rule Engine (Gemini unavailable)",
            "report_summary_hindi": hindi_map.get(severity, "विश्लेषण अनुपलब्ध"),
        }
    
    @property
    def is_available(self) -> bool:
        """Returns True if Gemini API is configured and ready."""
        return self._configured
    
    @property  
    def active_model(self) -> str:
        """Returns the name of the currently active model."""
        return self._active_model_name or "none"


# Module-level singleton
gemini_service = GeminiService()
