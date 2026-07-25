import email
import logging
from email import policy
from email.message import EmailMessage
from typing import Any, Dict

logger = logging.getLogger(__name__)

class EmailParserEngine:
    """
    Parses raw RFC 5322 email text into structured components.
    """
    
    @staticmethod
    def parse(raw_eml: str) -> Dict[str, Any]:
        try:
            # Parse using modern policy
            msg: EmailMessage = email.message_from_string(raw_eml, policy=policy.default)
            
            headers = {k: v for k, v in msg.items()}
            
            body_text = ""
            body_html = ""
            attachments = []
            
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Extract bodies
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body_text += part.get_content() or ""
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    body_html += part.get_content() or ""
                
                # Extract attachments
                if part.get_content_maintype() != 'multipart' and part.get_filename():
                    payload = part.get_payload(decode=True)
                    attachments.append({
                        "filename": part.get_filename(),
                        "content_type": content_type,
                        "size": len(payload) if payload else 0,
                        "raw_payload": payload
                    })
                    
            return {
                "headers": headers,
                "body_text": body_text,
                "body_html": body_html,
                "attachments": attachments,
                "error": None
            }
        except Exception as e:
            logger.error(f"Failed to parse email: {e}")
            return {"error": str(e)}
