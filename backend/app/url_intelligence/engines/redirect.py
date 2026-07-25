import httpx
from typing import List, Dict

class RedirectAnalysisEngine:
    """
    Analyzes URL redirect chains, detecting open redirects and capturing final landing pages.
    """
    
    @staticmethod
    async def analyze(url: str, max_depth: int = 10) -> List[Dict]:
        chain = []
        current_url = url
        
        async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
            for step in range(max_depth):
                try:
                    response = await client.get(current_url, follow_redirects=False)
                    status_code = response.status_code
                    
                    if 300 <= status_code < 400 and 'location' in response.headers:
                        next_url = response.headers['location']
                        # Handle relative redirects
                        if next_url.startswith('/'):
                            parsed = httpx.URL(current_url)
                            next_url = f"{parsed.scheme}://{parsed.host}{next_url}"
                            
                        chain.append({
                            "step_index": step + 1,
                            "from_url": current_url,
                            "to_url": next_url,
                            "status_code": status_code,
                            "redirect_type": "HTTP",
                            "response_time_ms": response.elapsed.total_seconds() * 1000
                        })
                        current_url = next_url
                    else:
                        # Reached final destination (or non-HTTP redirect like Meta refresh)
                        # We could parse HTML here for meta refresh or JS redirects, but for now we stop at HTTP
                        chain.append({
                            "step_index": step + 1,
                            "from_url": current_url,
                            "to_url": current_url,
                            "status_code": status_code,
                            "redirect_type": "FINAL",
                            "response_time_ms": response.elapsed.total_seconds() * 1000
                        })
                        break
                        
                except httpx.RequestError as exc:
                    chain.append({
                        "step_index": step + 1,
                        "from_url": current_url,
                        "to_url": None,
                        "status_code": None,
                        "redirect_type": "ERROR",
                        "error": str(exc)
                    })
                    break
                    
        return chain
