import re
from typing import List, Dict, Any

class JavaScriptAnalysisEngine:
    """
    Analyzes JavaScript for obfuscation, dynamic loading, tracking, and suspicious APIs.
    """
    
    SUSPICIOUS_APIS = ['eval', 'setTimeout', 'setInterval', 'document.write', 'Function', 'atob', 'btoa']
    TRACKING_DOMAINS = ['google-analytics.com', 'facebook.net', 'hotjar.com', 'clarity.ms']
    
    @classmethod
    def analyze(cls, scripts: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        results = []
        
        for script in scripts:
            is_obfuscated = False
            uses_suspicious_apis = False
            is_tracking = False
            accesses_clipboard = False
            makes_ajax = False
            
            src = script.get("src", "")
            content = script.get("content", "")
            
            # Check external script tracking
            if src:
                if any(domain in src for domain in cls.TRACKING_DOMAINS):
                    is_tracking = True
                    
            # Check inline content
            if content:
                # Basic obfuscation check (long strings of unreadable chars, excessive eval)
                if len(content) > 1000 and (content.count('eval(') > 3 or '\\x' in content or content.count('|') > 50):
                    is_obfuscated = True
                    
                if any(api + '(' in content for api in cls.SUSPICIOUS_APIS):
                    uses_suspicious_apis = True
                    
                if 'navigator.clipboard' in content or 'document.execCommand("copy")' in content:
                    accesses_clipboard = True
                    
                if 'fetch(' in content or 'XMLHttpRequest' in content:
                    makes_ajax = True
                    
            results.append({
                "script_source": src if src else "inline",
                "is_obfuscated": is_obfuscated,
                "makes_ajax_requests": makes_ajax,
                "accesses_clipboard": accesses_clipboard,
                "uses_suspicious_apis": uses_suspicious_apis,
                "is_tracking_library": is_tracking
            })
            
        return results
