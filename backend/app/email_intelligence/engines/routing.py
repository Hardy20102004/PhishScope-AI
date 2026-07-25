import re
from typing import Any, Dict, List


class RoutingAnalysisEngine:
    """
    Parses the Received header chain to reconstruct mail hops.
    """
    
    @staticmethod
    def analyze(headers: Dict[str, str]) -> List[Dict[str, Any]]:
        # In `email.message`, repeated headers might be lost if we just used `msg.items()` as a dict. 
        # In a robust implementation, we would extract all `Received` headers from the raw message.
        # For this prototype, if it's a string, we might just have the latest one, but we'll simulate a list if possible.
        
        # We will mock the hops based on the single string or list of strings if available
        received_raw = headers.get("Received") or headers.get("received")
        
        hops = []
        if not received_raw:
            return hops
            
        if isinstance(received_raw, str):
            received_list = [received_raw]
        else:
            received_list = received_raw
            
        # The Received chain is top-down (newest to oldest). 
        # For an investigation timeline, we want oldest (origin) to newest (destination).
        for idx, rec in enumerate(reversed(received_list)):
            # Basic parsing heuristic
            ip_match = re.search(r'\[([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\]', rec)
            sending_ip = ip_match.group(1) if ip_match else "unknown"
            
            hops.append({
                "hop_index": idx + 1,
                "receiving_server": "Mail Server", # Mocked
                "sending_server": "Upstream Relay", # Mocked
                "sending_ip": sending_ip,
                "timestamp": None, # Complex parsing required for RFC date
                "raw": rec
            })
            
        return hops
