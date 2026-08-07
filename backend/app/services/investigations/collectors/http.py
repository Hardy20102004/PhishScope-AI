from typing import Any, Dict

import httpx

from app.services.investigations.collectors.base import BaseCollector


class HTTPCollector(BaseCollector):
    
    def collect(self, target: str) -> Dict[str, Any]:
        evidence = {}
        try:
            # We want to capture the raw response body here as well for ContentCollector to use later,
            # but to keep collectors decoupled, they each do their own thing. 
            # In a true optimized architecture, a unified fetcher would grab the payload once.
            with httpx.Client(verify=False, timeout=5.0, follow_redirects=True) as client:
                response = client.get(target)
                
                redirects = []
                for r in response.history:
                    redirects.append({
                        "url": str(r.url),
                        "status_code": r.status_code
                    })
                
                evidence = {
                    "final_url": str(response.url),
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "redirect_chain": redirects,
                    "server": response.headers.get("server", "Unknown"),
                    "raw_body": response.text # Keep this to pass to ContentCollector if needed
                }
        except httpx.RequestError as e:
            evidence = {"error": f"HTTP Request failed: {str(e)}"}
            
        return evidence
