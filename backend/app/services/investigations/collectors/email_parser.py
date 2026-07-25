import email
from email import policy
from typing import Dict, Any, List
from app.services.investigations.collectors.base import BaseCollector

class EmailParserCollector(BaseCollector):
    
    def collect(self, target: str) -> Dict[str, Any]:
        """
        Parses a raw EML string.
        The `target` argument here should be the raw_content EML string.
        """
        if not target or len(target.strip()) == 0:
            return {"error": "No raw email content provided."}
            
        evidence: Dict[str, Any] = {
            "headers": {},
            "subject": "",
            "from": "",
            "to": "",
            "date": "",
            "message_id": "",
            "body_text": "",
            "body_html": "",
            "attachments": [],
            "urls_extracted": [] # will be populated later
        }
        
        try:
            # Parse the raw email using Python's modern email policy
            msg = email.message_from_string(target, policy=policy.default)
            
            # Extract basic headers
            evidence["subject"] = msg.get("Subject", "")
            evidence["from"] = msg.get("From", "")
            evidence["to"] = msg.get("To", "")
            evidence["date"] = msg.get("Date", "")
            evidence["message_id"] = msg.get("Message-ID", "")
            
            # Extract all headers for display
            for header, value in msg.items():
                if header not in evidence["headers"]:
                    evidence["headers"][header] = []
                evidence["headers"][header].append(value)
                
            # Extract Body and Attachments
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                
                # It's an attachment
                if "attachment" in content_disposition or part.get_filename():
                    filename = part.get_filename()
                    if filename:
                        payload = part.get_payload(decode=True)
                        size = len(payload) if payload else 0
                        evidence["attachments"].append({
                            "filename": filename,
                            "content_type": content_type,
                            "size_bytes": size
                        })
                    continue
                
                # It's the body
                if content_type == "text/plain" and not evidence["body_text"]:
                    evidence["body_text"] = part.get_content()
                elif content_type == "text/html" and not evidence["body_html"]:
                    evidence["body_html"] = part.get_content()
                    
        except Exception as e:
            evidence["error"] = f"Failed to parse email: {str(e)}"
            
        return evidence
