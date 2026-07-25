from typing import Any, Dict

from bs4 import BeautifulSoup

from app.services.investigations.collectors.base import BaseCollector


class ContentCollector(BaseCollector):
    
    def collect(self, target: str, html_body: str = "") -> Dict[str, Any]:
        """
        Content collector parses an HTML string.
        Since BaseCollector expects `target`, we add an optional `html_body` parameter.
        In the engine, we will pass the body collected by the HTTPCollector.
        """
        if not html_body:
            return {"error": "No HTML body provided to parse"}
            
        evidence = {
            "title": "",
            "meta_description": "",
            "forms_count": 0,
            "hidden_elements": 0,
            "suspicious_keywords_found": [],
            "scripts_count": 0
        }
        
        try:
            soup = BeautifulSoup(html_body, 'html.parser')
            
            # Title
            if soup.title:
                evidence["title"] = soup.title.string
                
            # Meta Description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                evidence["meta_description"] = meta_desc.get('content')
                
            # Forms
            forms = soup.find_all('form')
            evidence["forms_count"] = len(forms)
            
            # Hidden Elements (inputs)
            hidden_inputs = soup.find_all('input', type='hidden')
            evidence["hidden_elements"] = len(hidden_inputs)
            
            # Scripts
            scripts = soup.find_all('script')
            evidence["scripts_count"] = len(scripts)
            
            # Keyword Scan
            text_content = soup.get_text().lower()
            keywords = ['password', 'login', 'verify', 'wallet', 'seed phrase', 'credential']
            found = [kw for kw in keywords if kw in text_content]
            evidence["suspicious_keywords_found"] = found
            
        except Exception as e:
            evidence["error"] = f"HTML Parsing failed: {str(e)}"
            
        return evidence
