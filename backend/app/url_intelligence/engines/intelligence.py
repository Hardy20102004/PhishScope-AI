import math
from collections import Counter
import re

class URLIntelligenceEngine:
    """
    Analyzes URLs for structural anomalies, entropy, and suspicious patterns.
    """
    
    SUSPICIOUS_KEYWORDS = [
        "login", "signin", "secure", "account", "update", "verify", 
        "bank", "paypal", "auth", "confirm", "billing", "invoice", "wallet"
    ]
    
    @staticmethod
    def calculate_entropy(text: str) -> float:
        if not text:
            return 0.0
        counts = Counter(text)
        length = len(text)
        entropy = -sum((count/length) * math.log2(count/length) for count in counts.values())
        return entropy

    @classmethod
    def analyze(cls, url: str, parsed_url_dict: dict) -> dict:
        url_length = len(url)
        entropy = cls.calculate_entropy(url)
        
        found_keywords = [kw for kw in cls.SUSPICIOUS_KEYWORDS if kw in url.lower()]
        
        # Check for credential-like patterns (e.g. user:pass@)
        credential_pattern = False
        if '@' in parsed_url_dict.get('hostname', '') or ('@' in url and url.find('@') < url.find(parsed_url_dict.get('hostname', ''))):
             credential_pattern = True
             
        # Look for nested redirect parameters
        nested_redirect_params = []
        for param, values in parsed_url_dict.get('query_parameters', {}).items():
            for v in values:
                if v.startswith('http://') or v.startswith('https://'):
                    nested_redirect_params.append(param)
                    
        return {
            "url_length": url_length,
            "entropy": entropy,
            "suspicious_keywords_found": found_keywords,
            "credential_pattern": credential_pattern,
            "nested_redirect_parameters": nested_redirect_params
        }
