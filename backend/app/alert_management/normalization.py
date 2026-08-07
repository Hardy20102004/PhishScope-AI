import uuid
from typing import Any, Dict, List
from datetime import datetime, timezone

class AlertNormalizationEngine:
    """
    Normalizes alerts from disparate sources (EDR, SIEM, Firewalls)
    into a standardized internal format.
    """
    
    @staticmethod
    def normalize_severity(raw_severity: str) -> str:
        """Standardizes severity levels across vendors."""
        raw = str(raw_severity).strip().upper()
        if raw in ["1", "LOW", "INFO", "INFORMATIONAL"]:
            return "LOW"
        if raw in ["2", "MEDIUM", "MODERATE"]:
            return "MEDIUM"
        if raw in ["3", "HIGH", "SEVERE"]:
            return "HIGH"
        if raw in ["4", "5", "CRITICAL", "FATAL"]:
            return "CRITICAL"
        return "MEDIUM" # Default fallback
    
    @staticmethod
    def extract_evidence(raw_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extracts standard evidence artifacts (IP, hashes, domains) from common raw schema structures."""
        evidence = []
        
        # Example logic for common schema layouts
        if "source_ip" in raw_payload:
            evidence.append({"evidence_type": "IP", "value": raw_payload["source_ip"]})
        if "destination_ip" in raw_payload:
            evidence.append({"evidence_type": "IP", "value": raw_payload["destination_ip"]})
        if "file_hash" in raw_payload:
            evidence.append({"evidence_type": "HASH", "value": raw_payload["file_hash"]})
        if "domain" in raw_payload:
            evidence.append({"evidence_type": "DOMAIN", "value": raw_payload["domain"]})
        if "user_name" in raw_payload:
            evidence.append({"evidence_type": "USER", "value": raw_payload["user_name"]})
            
        # Additional parsing could handle CEF, LEEF formats here.
        return evidence

    @classmethod
    def normalize_alert(cls, raw_payload: Dict[str, Any], source: str, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """
        Parses an incoming raw JSON payload into our standard Alert schema.
        """
        severity = cls.normalize_severity(raw_payload.get("severity", "MEDIUM"))
        evidence = cls.extract_evidence(raw_payload)
        
        normalized = {
            "title": raw_payload.get("title", f"Alert from {source}"),
            "description": raw_payload.get("description", ""),
            "source": source,
            "source_alert_id": str(raw_payload.get("id", uuid.uuid4())),
            "category": raw_payload.get("category", "General"),
            "severity": severity,
            "tenant_id": tenant_id,
            "evidence": evidence
        }
        
        return normalized
