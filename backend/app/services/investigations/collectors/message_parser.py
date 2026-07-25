import re
from typing import Dict, Any
from app.services.investigations.collectors.base import BaseCollector

class MessageParserCollector(BaseCollector):
    
    def collect(self, target: str) -> Dict[str, Any]:
        """
        Parses raw SMS/WhatsApp text to extract URLs and Phone Numbers.
        """
        if not target or len(target.strip()) == 0:
            return {"error": "No raw message provided."}
            
        evidence: Dict[str, Any] = {
            "raw_text": target,
            "urls": [],
            "phone_numbers": [],
            "emails": []
        }
        
        # Extract URLs
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w.-]*')
        evidence["urls"] = list(set(url_pattern.findall(target)))
        
        # Extract basic phone numbers (rudimentary regex for MVP)
        phone_pattern = re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}')
        phones = phone_pattern.findall(target)
        # Filter out obvious false positives like dates or short numbers
        evidence["phone_numbers"] = list(set([p.strip() for p in phones if len(re.sub(r'\D', '', p)) >= 7]))
        
        # Extract emails
        email_pattern = re.compile(r'[\w.-]+@[\w.-]+\.\w+')
        evidence["emails"] = list(set(email_pattern.findall(target)))
        
        return evidence
