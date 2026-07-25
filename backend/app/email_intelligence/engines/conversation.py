import re
from typing import Dict, Any, List

class ConversationAnalysisEngine:
    """
    Analyzes the text/html body for urgency indicators, impersonation signs (BEC), and extracts URLs.
    """
    
    URGENCY_KEYWORDS = ["urgent", "immediate action required", "overdue", "final notice", "wire transfer", "gift card", "invoice"]
    
    @classmethod
    def analyze(cls, body_text: str, body_html: str) -> Dict[str, Any]:
        text_lower = (body_text + body_html).lower()
        
        urgency_score = sum(1 for kw in cls.URGENCY_KEYWORDS if kw in text_lower)
        is_bec_suspect = urgency_score > 0 and ("wire" in text_lower or "gift card" in text_lower or "invoice" in text_lower)
        
        # Extract URLs (very naive regex for prototype)
        # Note: in a real system we would parse HTML hrefs robustly.
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        extracted_urls_raw = re.findall(url_pattern, text_lower)
        extracted_urls = list(set(extracted_urls_raw)) # Deduplicate
        
        formatted_urls = [{"url": u, "context": "body"} for u in extracted_urls]
        
        return {
            "urgency_indicators_found": urgency_score,
            "is_bec_suspect": is_bec_suspect,
            "extracted_urls": formatted_urls
        }
