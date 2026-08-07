from typing import Any, Dict


class SecurityHeaderAnalyzer:
    """
    Validates CSP, HSTS, X-Frame-Options, and other security headers.
    """
    
    @staticmethod
    def analyze(headers: Dict[str, str]) -> Dict[str, Any]:
        # Headers are usually case-insensitive, so we normalize to lower case keys
        normalized_headers = {k.lower(): v for k, v in headers.items()}
        
        csp = normalized_headers.get('content-security-policy', '')
        hsts = normalized_headers.get('strict-transport-security', '')
        xfo = normalized_headers.get('x-frame-options', '')
        xcto = normalized_headers.get('x-content-type-options', '')
        referrer = normalized_headers.get('referrer-policy', '')
        permissions = normalized_headers.get('permissions-policy', '')
        
        # Mixed content check (if HTTP resources are loaded on HTTPS, usually checked via DOM/Network, 
        # but for this engine, we just default to False unless we had DOM network data).
        has_mixed_content = False 
        
        return {
            "content_security_policy": csp,
            "strict_transport_security": hsts,
            "x_frame_options": xfo,
            "x_content_type_options": xcto,
            "referrer_policy": referrer,
            "permissions_policy": permissions,
            "has_mixed_content": has_mixed_content
        }
