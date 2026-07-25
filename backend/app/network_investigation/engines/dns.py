from typing import Dict, Any, List

class DNSAnalysisEngine:
    @staticmethod
    def extract(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        dns_logs = parsed_data.get("dns", [])
        dns_records = []
        
        suspicious_keywords = ["c2", "beacon", "malicious", "evil", "crypto"]
        
        for d in dns_logs:
            query = d.get("query", "")
            is_suspicious = any(kw in query.lower() for kw in suspicious_keywords)
            
            dns_records.append({
                "timestamp": d.get("ts"),
                "query": query,
                "record_type": d.get("qtype_name"),
                "response_code": d.get("rcode_name"),
                "answers": d.get("answers", []),
                "is_malicious": is_suspicious
            })
        return dns_records
