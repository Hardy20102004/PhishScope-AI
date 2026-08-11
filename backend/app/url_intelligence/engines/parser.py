from urllib.parse import parse_qs, urlparse

try:
    import tldextract
    _HAS_TLDEXTRACT = True
except ImportError:
    _HAS_TLDEXTRACT = False


class URLParser:
    """
    Parses URLs into detailed components compliant with RFC standards.
    
    Fixed (v2):
    - BUG-007: Now uses tldextract for correct multi-level TLD parsing.
      Previously, naive hostname.split('.') would break for domains like:
        - example.co.uk → was: subdomain=example, root=co.uk (WRONG)
        - example.gov.in → was: subdomain=example, root=gov.in (WRONG)
        - example.ac.in  → same bug — critical for UP Police .gov.in domains
      
      With tldextract:
        - example.co.uk → subdomain='', domain='example', suffix='co.uk' ✓
        - sbionlineservices.gov.in → domain='sbionlineservices', suffix='gov.in' ✓
    """
    
    @staticmethod
    def parse(url: str) -> dict:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        
        if _HAS_TLDEXTRACT and hostname:
            # Correct multi-level TLD extraction (handles .gov.in, .co.uk, .ac.in etc.)
            extracted = tldextract.extract(hostname)
            subdomain = extracted.subdomain
            domain_name = extracted.domain
            public_suffix = extracted.suffix
            
            if domain_name and public_suffix:
                root_domain = f"{domain_name}.{public_suffix}"
            elif domain_name:
                root_domain = domain_name
            else:
                root_domain = hostname
        else:
            # Fallback: naive split (less accurate for multi-level TLDs)
            parts = hostname.split('.')
            if len(parts) > 2:
                subdomain = ".".join(parts[:-2])
                root_domain = ".".join(parts[-2:])
                public_suffix = parts[-1]
            elif len(parts) == 2:
                subdomain = ""
                root_domain = hostname
                public_suffix = parts[-1]
            else:
                subdomain = ""
                root_domain = hostname
                public_suffix = ""

        # Check encodings
        encoded_chars = '%' in url
        unicode_chars = any(ord(char) > 127 for char in url)
        
        query_params = parse_qs(parsed.query)
        
        # Determine default port
        if parsed.port:
            port = parsed.port
        elif parsed.scheme == "https":
            port = 443
        elif parsed.scheme == "http":
            port = 80
        else:
            port = None

        return {
            "protocol": parsed.scheme,
            "hostname": hostname,
            "subdomain": subdomain,
            "root_domain": root_domain,
            "public_suffix": public_suffix,
            "port": port,
            "path": parsed.path,
            "query_parameters": query_params,
            "fragments": parsed.fragment,
            "encoded_characters": encoded_chars,
            "unicode_characters": unicode_chars,
            "tldextract_available": _HAS_TLDEXTRACT,
        }
