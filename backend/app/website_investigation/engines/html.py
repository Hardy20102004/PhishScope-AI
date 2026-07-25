from bs4 import BeautifulSoup

class HTMLAnalysisEngine:
    """
    Analyzes HTML structure, identifying hidden elements, iframes, meta refreshes, and suspicious tags.
    """
    
    @staticmethod
    def analyze(html: str) -> dict:
        if not html:
            return {
                "has_hidden_elements": False,
                "has_iframes": False,
                "has_meta_refresh": False,
                "has_suspicious_tags": False,
                "embedded_credentials": False
            }
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check for hidden elements (inline CSS hiding)
        has_hidden = False
        for tag in soup.find_all(style=True):
            style = tag['style'].lower()
            if 'display: none' in style or 'display:none' in style or 'visibility: hidden' in style or 'visibility:hidden' in style:
                has_hidden = True
                break
                
        # Check for iframes
        has_iframes = len(soup.find_all('iframe')) > 0
        
        # Check for meta refresh
        has_meta_refresh = False
        for meta in soup.find_all('meta'):
            if meta.get('http-equiv', '').lower() == 'refresh':
                has_meta_refresh = True
                break
                
        # Suspicious tags (e.g., base tag pointing to different domain, or unescaped scripts)
        has_suspicious_tags = len(soup.find_all('base')) > 0
        
        # Embedded credentials in HTML comments or hidden fields
        embedded_creds = False
        for comment in soup.find_all(string=lambda text: isinstance(text, str)):
            text = comment.lower()
            if 'password' in text and ('=' in text or ':' in text):
                # Rough heuristic
                embedded_creds = True
                
        return {
            "has_hidden_elements": has_hidden,
            "has_iframes": has_iframes,
            "has_meta_refresh": has_meta_refresh,
            "has_suspicious_tags": has_suspicious_tags,
            "embedded_credentials": embedded_creds
        }
