import base64
import io
from typing import Dict, Any
from app.services.investigations.collectors.base import BaseCollector

class QRDecoderCollector(BaseCollector):
    
    def collect(self, target: str) -> Dict[str, Any]:
        """
        Takes a Base64 encoded image string (data URI or raw base64), 
        decodes the QR code, and returns the payload.
        """
        evidence: Dict[str, Any] = {
            "decoded_text": None,
            "format": None,
            "error": None
        }
        
        if not target:
            evidence["error"] = "No Base64 image provided."
            return evidence
            
        try:
            from PIL import Image
            from pyzbar.pyzbar import decode, ZBarSymbol
        except ImportError:
            evidence["error"] = "QR Decoder dependencies (Pillow, pyzbar) are not installed or C-library is missing."
            return evidence
            
        try:
            # Strip data URI prefix if present (e.g. "data:image/png;base64,")
            if "," in target:
                b64_data = target.split(",")[1]
            else:
                b64_data = target
                
            image_data = base64.b64decode(b64_data)
            image = Image.open(io.BytesIO(image_data))
            
            # Decode the QR code
            decoded_objects = decode(image, symbols=[ZBarSymbol.QRCODE])
            
            if not decoded_objects:
                evidence["error"] = "No QR code found in the image."
                return evidence
                
            # We assume one QR code per image for now
            obj = decoded_objects[0]
            evidence["decoded_text"] = obj.data.decode('utf-8')
            evidence["format"] = obj.type
            
        except Exception as e:
            evidence["error"] = f"Failed to decode image: {str(e)}"
            
        return evidence
