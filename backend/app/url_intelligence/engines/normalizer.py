import urllib.parse
from posixpath import normpath


class URLNormalizationEngine:
    """
    Normalizes URLs for canonical representation and deduplication.
    """
    
    @staticmethod
    def normalize(url: str) -> str:
        # 1. Percent-decoding and Parse
        parsed = urllib.parse.urlparse(urllib.parse.unquote(url))
        
        # 2. Lowercase protocol and hostname
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        
        # 3. Path Normalization (remove /./ and /../)
        path = parsed.path
        if path:
            path = normpath(path)
            if not path.startswith('/'):
                path = '/' + path
                
        # 4. Parameter Ordering and Duplicate Removal
        query = parsed.query
        if query:
            query_params = urllib.parse.parse_qsl(query, keep_blank_values=True)
            # Remove duplicates by using dict, then sort by key
            unique_params = {}
            for k, v in query_params:
                if k not in unique_params:
                    unique_params[k] = v
            sorted_query = urllib.parse.urlencode(sorted(unique_params.items()))
        else:
            sorted_query = ""
            
        # Reconstruct canonical URL (dropping fragment usually for canonicalization)
        canonical_url = urllib.parse.urlunparse((
            scheme,
            netloc,
            path,
            parsed.params,
            sorted_query,
            "" # fragment
        ))
        
        return canonical_url
