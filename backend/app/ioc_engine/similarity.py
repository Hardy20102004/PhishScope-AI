from typing import Optional
from app.models.threat_intel import IOCType
import difflib

class SimilarityEngine:
    """
    Handles similarity and fuzzy matching between IOCs.
    """

    @staticmethod
    def calculate_similarity(value1: str, value2: str, ioc_type: IOCType) -> float:
        """
        Calculates similarity score between 0.0 and 1.0.
        """
        if value1 == value2:
            return 1.0

        if ioc_type in (IOCType.DOMAIN, IOCType.SUBDOMAIN):
            return SimilarityEngine._domain_similarity(value1, value2)
            
        if ioc_type == IOCType.URL:
            return SimilarityEngine._url_similarity(value1, value2)

        if ioc_type in (IOCType.SHA256, IOCType.MD5, IOCType.SHA1, IOCType.IPV4, IOCType.IPV6):
            return 1.0 if value1 == value2 else 0.0 # Hashes and IPs must be exact match

        # Fallback to string distance
        return difflib.SequenceMatcher(None, value1, value2).ratio()

    @staticmethod
    def _domain_similarity(d1: str, d2: str) -> float:
        """
        Levenshtein distance for domains. Good for catching typosquatting.
        """
        return difflib.SequenceMatcher(None, d1, d2).ratio()
        
    @staticmethod
    def _url_similarity(u1: str, u2: str) -> float:
        """
        Structural similarity for URLs (ignoring query params, matching path structure).
        """
        # For a full implementation, we would parse the URL and compare netloc and path independently
        # and weight them differently. For now, simple string distance.
        return difflib.SequenceMatcher(None, u1, u2).ratio()
