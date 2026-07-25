import hashlib
from typing import List, Dict, Any

class AttachmentIntelligenceEngine:
    """
    Extracts attachment metadata and computes hashes.
    """
    
    @staticmethod
    def analyze(attachments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for att in attachments:
            payload = att.get("raw_payload", b"")
            sha256_hash = hashlib.sha256(payload).hexdigest() if payload else ""
            
            filename = att.get("filename", "")
            is_suspicious = False
            
            # Simple heuristic
            if filename.endswith(".exe") or filename.endswith(".vbs") or filename.endswith(".scr") or filename.endswith(".iso"):
                is_suspicious = True
                
            results.append({
                "filename": filename,
                "content_type": att.get("content_type", ""),
                "size_bytes": att.get("size", 0),
                "sha256_hash": sha256_hash,
                "is_suspicious": is_suspicious
            })
            
        return results
