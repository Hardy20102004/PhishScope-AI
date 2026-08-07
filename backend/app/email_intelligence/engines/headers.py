from typing import Any, Dict


class HeaderAnalysisEngine:
    """
    Extracts and normalizes critical fields from parsed headers.
    """
    
    @staticmethod
    def analyze(headers: Dict[str, str]) -> Dict[str, Any]:
        # email.message items often have multiple keys if repeated, 
        # but for simplicity, we assume dictionary with latest/first value here depending on parser.
        
        # Normalize keys to lowercase for safe lookup
        normalized_headers = {k.lower(): str(v) for k, v in headers.items()}
        
        def parse_addresses(addr_str: str) -> list:
            if not addr_str: return []
            # Very naive split, usually standard library email.utils.getaddresses is better
            return [a.strip() for a in addr_str.split(',')]
            
        return {
            "message_id": normalized_headers.get("message-id", ""),
            "date_sent": normalized_headers.get("date", ""),
            "subject": normalized_headers.get("subject", ""),
            "from_address": normalized_headers.get("from", ""),
            "return_path": normalized_headers.get("return-path", ""),
            "reply_to": normalized_headers.get("reply-to", ""),
            "to_addresses": parse_addresses(normalized_headers.get("to", "")),
            "cc_addresses": parse_addresses(normalized_headers.get("cc", "")),
            "raw_headers": headers
        }
