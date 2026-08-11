import base64
import io
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict

from app.services.investigations.collectors.base import BaseCollector


class QRDecoderCollector(BaseCollector):
    
    def collect(self, target: str) -> Dict[str, Any]:
        """
        Takes a Base64 encoded image string, raw URL, or SVG payload,
        decodes the QR code or payload, and returns the payload.
        
        Fixes applied:
        - OpenCV cv2.QRCodeDetector() used as primary (no C-library libzbar required)
        - pyzbar fallback if available
        - Direct SVG XML link/text extraction if target is SVG
        - Raw URL string detection fallback
        """
        evidence: Dict[str, Any] = {
            "decoded_text": None,
            "format": None,
            "error": None
        }
        
        if not target:
            evidence["error"] = "No image or payload provided."
            return evidence
            
        # 1. Check if target is already a raw HTTP/HTTPS URL or text payload
        if target.startswith(("http://", "https://", "upi://", "mailto:", "tel:")):
            evidence["decoded_text"] = target.strip()
            evidence["format"] = "TEXT/URL"
            return evidence
            
        # Strip data URI prefix if present (e.g. "data:image/png;base64,")
        b64_data = target.split(",")[1] if "," in target else target
        
        raw_bytes = None
        try:
            raw_bytes = base64.b64decode(b64_data)
        except Exception:
            # If not valid base64, check if it's plain text XML/SVG or text string
            if "<svg" in target.lower():
                raw_bytes = target.encode("utf-8")
            else:
                evidence["decoded_text"] = target.strip()
                evidence["format"] = "RAW_STRING"
                return evidence
                
        # 2. SVG XML Parsing (for SVG QR codes like QR_code_for_mobile_English_Wikipedia.svg)
        if raw_bytes and b"<svg" in raw_bytes.lower():
            try:
                text_content = raw_bytes.decode("utf-8", errors="ignore")
                # Look for href links in SVG (e.g. <a href="http..."> or xlink:href)
                urls = re.findall(r'(?:href|xlink:href)=["\'](https?://[^"\']+|upi://[^"\']+)["\']', text_content)
                if urls:
                    evidence["decoded_text"] = urls[0]
                    evidence["format"] = "SVG_EMBEDDED_URL"
                    return evidence
                # Look for text tags in SVG
                texts = re.findall(r'<text[^>]*>([^<]+)</text>', text_content)
                if texts:
                    evidence["decoded_text"] = " ".join(texts).strip()
                    evidence["format"] = "SVG_TEXT"
                    return evidence
            except Exception:
                pass

        # 3. Decode raster image using OpenCV (Primary - no system libzbar required)
        try:
            import cv2
            import numpy as np
            from PIL import Image

            pil_img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
            cv_img = np.array(pil_img)[:, :, ::-1].copy()  # RGB to BGR for OpenCV
            
            detector = cv2.QRCodeDetector()
            decoded_text, points, _ = detector.detectAndDecode(cv_img)
            
            if decoded_text:
                evidence["decoded_text"] = decoded_text
                evidence["format"] = "QR_CODE"
                return evidence
        except Exception as cv_err:
            pass

        # 4. Fallback to pyzbar (if zbar C library installed)
        try:
            from PIL import Image
            from pyzbar.pyzbar import ZBarSymbol, decode
            pil_img = Image.open(io.BytesIO(raw_bytes))
            decoded_objects = decode(pil_img, symbols=[ZBarSymbol.QRCODE])
            if decoded_objects:
                obj = decoded_objects[0]
                evidence["decoded_text"] = obj.data.decode('utf-8')
                evidence["format"] = str(obj.type)
                return evidence
        except Exception:
            pass
            
        # If we reached here, no QR payload was extracted
        evidence["error"] = "No valid QR code or URL payload detected in the provided file."
        return evidence
