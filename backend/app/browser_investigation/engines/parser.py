import json
from typing import Dict, Any

class ProfileParserEngine:
    """
    Simulates parsing browser forensic exports (History/Cookies SQLite).
    """
    
    @staticmethod
    def parse(payload: str) -> Dict[str, Any]:
        try:
            data = json.loads(payload)
            return data
        except:
            # Fallback mock for testing
            return {
                "history": [
                    {"url": "https://www.google.com/search?q=free+bitcoin", "title": "Google Search", "visit_time": "2024-01-01T10:00:00Z", "visit_count": 1, "is_search": True, "search_keyword": "free bitcoin"},
                    {"url": "http://evil-crypto-drop.com/installer.exe", "title": "Download Installer", "visit_time": "2024-01-01T10:05:00Z", "visit_count": 1, "is_search": False}
                ],
                "cookies": [
                    {"domain": ".evil-crypto-drop.com", "name": "session_id", "creation_time": "2024-01-01T10:05:05Z", "is_secure": False, "is_httponly": False}
                ],
                "extensions": [
                    {"name": "AdBlock Plus", "extension_id": "cfhdojbkjhnklbpkdaibdccddilifddb", "permissions": ["storage", "webRequest"], "is_suspicious": False},
                    {"name": "Bitcoin Miner Pro", "extension_id": "malicious_ext_123", "permissions": ["tabs", "<all_urls>"], "is_suspicious": True}
                ],
                "downloads": [
                    {"filename": "installer.exe", "source_url": "http://evil-crypto-drop.com/installer.exe", "download_time": "2024-01-01T10:06:00Z", "file_size": 1048576, "is_malicious": True}
                ]
            }
