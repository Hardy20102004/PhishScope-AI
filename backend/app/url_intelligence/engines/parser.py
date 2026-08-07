from urllib.parse import parse_qs, urlparse


class URLParser:
    """
    Parses URLs into detailed components compliant with RFC standards.
    """
    
    @staticmethod
    def parse(url: str) -> dict:
        parsed = urlparse(url)
        
        hostname = parsed.hostname or ""
        
        # Simple extraction for domain/subdomain without tldextract
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

        return {
            "protocol": parsed.scheme,
            "hostname": hostname,
            "subdomain": subdomain,
            "root_domain": root_domain,
            "public_suffix": public_suffix,
            "port": parsed.port or (443 if parsed.scheme == "https" else 80 if parsed.scheme == "http" else None),
            "path": parsed.path,
            "query_parameters": query_params,
            "fragments": parsed.fragment,
            "encoded_characters": encoded_chars,
            "unicode_characters": unicode_chars
        }
