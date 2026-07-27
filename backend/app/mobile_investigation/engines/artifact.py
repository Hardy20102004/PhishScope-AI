import json
from typing import Any, Dict


class ArtifactProcessingEngine:
    """
    Simulates parsing forensic exports (JSON, XML, SQLite).
    """
    
    @staticmethod
    def parse(payload: str) -> Dict[str, Any]:
        try:
            # If the payload is JSON (mocked), parse it
            data = json.loads(payload)
            return data
        except Exception:
            # Fallback mock for non-JSON strings (prototype behavior)
            return {
                "device_metadata": {
                    "manufacturer": "Google",
                    "model": "Pixel 7 Pro",
                    "os_name": "Android",
                    "os_version": "14",
                    "timezone": "UTC-5"
                },
                "applications": [
                    {"app_name": "WhatsApp", "package_name": "com.whatsapp", "permissions": ["SMS", "Location"], "is_suspicious": False},
                    {"app_name": "Free Games Hub", "package_name": "com.evil.games", "permissions": ["SMS", "Contacts", "Admin"], "is_suspicious": True}
                ],
                "communications": [
                    {"comm_type": "SMS", "direction": "Incoming", "contact_number": "+15551234567", "body": "Click here to secure your account: http://evil-login-update.com", "timestamp": "2024-01-01T10:00:00Z"}
                ],
                "locations": [
                    {"latitude": 40.7128, "longitude": -74.0060, "timestamp": "2024-01-01T08:30:00Z", "source": "GPS", "label": "Coffee Shop"}
                ]
            }
