from typing import Any, Dict


class QRDecoderEngine:
    """
    Simulates extracting standard URLs, text, Wi-Fi configs, and Custom Payloads from a QR image.
    In production, this wraps libraries like pyzbar or OpenCV's QRCodeDetector.
    """
    
    @staticmethod
    def decode(image_payload: str) -> Dict[str, Any]:
        # For the prototype, we expect `image_payload` to be a string representing the decoded 
        # text for testing purposes, or we mock it if it's base64 image data.
        
        raw_text = image_payload
        payload_type = "text"
        extracted_url = None
        
        # Simple heuristics to categorize payload
        if raw_text.startswith("http://") or raw_text.startswith("https://"):
            payload_type = "url"
            extracted_url = raw_text
        elif raw_text.startswith("upi://pay"):
            payload_type = "payment_upi"
        elif raw_text.startswith("WIFI:"):
            payload_type = "wifi"
        elif raw_text.startswith("MECARD:") or raw_text.startswith("BEGIN:VCARD"):
            payload_type = "contact"
            
        return {
            "raw_payload": raw_text,
            "payload_type": payload_type,
            "extracted_url": extracted_url
        }
