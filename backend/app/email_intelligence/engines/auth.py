from typing import Any, Dict


class AuthenticationAnalysisEngine:
    """
    Evaluates the Authentication-Results header and extracts SPF, DKIM, and DMARC alignment status.
    """
    
    @staticmethod
    def analyze(headers: Dict[str, str]) -> Dict[str, Any]:
        # Typical header looks like:
        # Authentication-Results: mx.google.com; spf=pass (google.com: domain of sender@example.com designates 1.2.3.4 as permitted sender) smtp.mailfrom=sender@example.com; dkim=pass header.i=@example.com; dmarc=pass (p=REJECT sp=NONE dis=NONE) header.from=example.com
        
        normalized_headers = {k.lower(): str(v) for k, v in headers.items()}
        auth_results_raw = normalized_headers.get("authentication-results", "").lower()
        
        spf_result = "unknown"
        dkim_result = "unknown"
        dmarc_result = "unknown"
        is_spoofed = False
        
        if auth_results_raw:
            if "spf=pass" in auth_results_raw: spf_result = "pass"
            elif "spf=fail" in auth_results_raw or "spf=softfail" in auth_results_raw: spf_result = "fail"
            
            if "dkim=pass" in auth_results_raw: dkim_result = "pass"
            elif "dkim=fail" in auth_results_raw: dkim_result = "fail"
            
            if "dmarc=pass" in auth_results_raw: dmarc_result = "pass"
            elif "dmarc=fail" in auth_results_raw: dmarc_result = "fail"
            
        if spf_result == "fail" or dmarc_result == "fail":
            is_spoofed = True
            
        return {
            "spf_result": spf_result,
            "dkim_result": dkim_result,
            "dmarc_result": dmarc_result,
            "is_spoofed": is_spoofed,
            "raw_auth_header": auth_results_raw
        }
