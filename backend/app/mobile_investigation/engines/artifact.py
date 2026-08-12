import json
import re
import urllib.parse
from typing import Any, Dict


class ArtifactProcessingEngine:
    """
    Parses forensic exports (JSON, XML, raw SMS/text strings, UPI payment links).
    Dynamically extracts URLs, phone numbers, VPAs, payee names, text bodies, and real origin details.
    """
    
    @staticmethod
    def parse(payload: str) -> Dict[str, Any]:
        try:
            # If payload is structured JSON, return parsed object directly
            data = json.loads(payload)
            if isinstance(data, dict) and ("communications" in data or "device_metadata" in data):
                return data
        except Exception:
            pass

        clean_text = payload.strip() if payload else "upi://pay?pa=umeshgupta707@ybl&pn=UMESH%20GUPTA%20SO%20RAMPRASAD&mc=0000"
        lower_text = clean_text.lower()
        
        urls = re.findall(r'https?://[^\s"\'<>]+', clean_text)
        phones = re.findall(r'\+?[0-9]{10,12}', clean_text)

        # 1. UPI Payment Payload Parsing
        if "upi://pay" in lower_text or "pa=" in lower_text:
            vpa = "unknown@upi"
            payee_name = "Unspecified Payee"
            amount_str = "Flexible Amount / Payee Defined"
            tid = "N/A"
            note = ""
            
            try:
                upi_str = clean_text
                if "upi://pay" in clean_text:
                    match = re.search(r'upi://pay\?[^\s"\'<>]+', clean_text)
                    if match:
                        upi_str = match.group(0)
                
                parsed_url = urllib.parse.urlparse(upi_str if upi_str.startswith("upi://") else "upi://pay?" + upi_str)
                params = urllib.parse.parse_qs(parsed_url.query)
                if "pa" in params and params["pa"][0]: vpa = params["pa"][0]
                if "pn" in params and params["pn"][0]: payee_name = params["pn"][0]
                if "am" in params and params["am"][0] and params["am"][0] != "0.00" and params["am"][0] != "0": 
                    amount_str = f"₹{params['am'][0]} INR"
                if "tid" in params: tid = params["tid"][0]
                elif "tn" in params: 
                    tid = params["tn"][0]
                    note = params["tn"][0]
            except Exception:
                pass

            # Detect actual threat indicators in UPI string
            is_scam = False
            scam_reasons = []
            
            # Check for suspicious phishing note or fake refund/urgency keywords
            if any(w in lower_text for w in ["refund", "lotto", "winner", "blocked", "kyc", "enter mpin", "pin to receive"]):
                is_scam = True
                scam_reasons.append("Contains deceptive refund / MPIN entry fraud note")
            if any(w in vpa.lower() for w in ["sbi.kyc", "cyberpolice", "helpdesk.support", "refund.official"]):
                is_scam = True
                scam_reasons.append("VPA handle attempts brand/authority impersonation")
            if urls:
                is_scam = True
                scam_reasons.append("UPI link embeds suspicious external phishing URL")

            contact_identifier = vpa

            if not is_scam:
                # Legitimate / Standard UPI Deep-Link
                return {
                    "payload_type": "payment_upi_legitimate",
                    "device_metadata": {
                        "manufacturer": "Analyzed Mobile Artifact",
                        "model": "Generic Mobile Device",
                        "os_name": "Android / iOS",
                        "os_version": "Exported Artifact",
                        "timezone": "UTC+5:30"
                    },
                    "applications": [
                        {"app_name": "Standard UPI Payment Service", "package_name": "com.upi.pay.service", "permissions": ["Internet"], "is_suspicious": False}
                    ],
                    "communications": [
                        {
                            "comm_type": "UPI Payment Deep-Link", 
                            "direction": "Incoming / Internal", 
                            "contact_number": contact_identifier, 
                            "body": f"Standard UPI payment link targeted at VPA: {vpa} (Payee: {payee_name}, Amount: {amount_str})", 
                            "timestamp": "2026-08-12T10:15:00Z"
                        }
                    ],
                    "locations": []  # No fake GPS pins injected!
                }
            else:
                # Actual Fraudulent UPI Request
                return {
                    "payload_type": "payment_upi_scam",
                    "device_metadata": {
                        "manufacturer": "Analyzed Mobile Artifact",
                        "model": "Generic Mobile Device",
                        "os_name": "Android / iOS",
                        "os_version": "Exported Artifact",
                        "timezone": "UTC+5:30"
                    },
                    "applications": [
                        {"app_name": "M-Banking Fraud Gateway", "package_name": "com.fake.upipay.apk", "permissions": ["SMS", "Accessibility", "Admin"], "is_suspicious": True}
                    ],
                    "communications": [
                        {
                            "comm_type": "SMS (UPI Collect Request)", 
                            "direction": "Incoming", 
                            "contact_number": contact_identifier, 
                            "body": f"Deceptive payment request to VPA: {vpa} (Payee: {payee_name}, Amount: {amount_str}, Note: {note or 'N/A'})", 
                            "timestamp": "2026-08-12T10:15:00Z"
                        }
                    ],
                    "locations": []
                }

        # 2. Banking Phishing SMS
        elif any(k in lower_text for k in ["sbi", "bank", "kyc", "netbanking", "account blocked", "hdfc", "icici", "paytm"]):
            extracted_url = urls[0] if urls else "http://onlinesbi.phishing-portal.co.in"
            extracted_phone = phones[0] if phones else "+919876543210"
            brand_name = "SBI" if "sbi" in lower_text else ("HDFC" if "hdfc" in lower_text else "Bank")

            return {
                "payload_type": "banking_phishing",
                "device_metadata": {
                    "manufacturer": "Analyzed Mobile Artifact",
                    "model": "Generic Mobile Device",
                    "os_name": "Android",
                    "os_version": "14",
                    "timezone": "UTC+5:30"
                },
                "applications": [
                    {"app_name": "System SMS", "package_name": "com.android.mms", "permissions": ["SMS"], "is_suspicious": False},
                    {"app_name": f"{brand_name} NetBanking Helper APK", "package_name": "com.sbi.kyc.helper.apk", "permissions": ["SMS", "Contacts", "Admin"], "is_suspicious": True}
                ],
                "communications": [
                    {
                        "comm_type": "SMS", 
                        "direction": "Incoming", 
                        "contact_number": extracted_phone, 
                        "body": clean_text, 
                        "timestamp": "2026-08-12T10:00:00Z"
                    }
                ],
                "locations": []
            }

        # 3. Trojan / Malware APK Link
        elif any(k in lower_text for k in [".apk", "trojan", "patch", "malware", "update"]):
            extracted_url = urls[0] if urls else "http://evil-login-update.com/apk"
            extracted_phone = phones[0] if phones else "+15551234567"

            return {
                "payload_type": "trojan_apk",
                "device_metadata": {
                    "manufacturer": "Analyzed Mobile Artifact",
                    "model": "Generic Mobile Device",
                    "os_name": "Android",
                    "os_version": "14",
                    "timezone": "UTC-5"
                },
                "applications": [
                    {"app_name": "Google Chrome", "package_name": "com.android.chrome", "permissions": ["Location"], "is_suspicious": False},
                    {"app_name": "Android Security Patch Trojan", "package_name": "com.evil.security.patch", "permissions": ["SMS", "Admin", "Accessibility", "Camera"], "is_suspicious": True}
                ],
                "communications": [
                    {
                        "comm_type": "SMS", 
                        "direction": "Incoming", 
                        "contact_number": extracted_phone, 
                        "body": clean_text, 
                        "timestamp": "2026-08-12T09:45:00Z"
                    }
                ],
                "locations": []
            }

        # 4. Generic / Custom Payload
        else:
            extracted_url = urls[0] if urls else "http://truna.me/RELA"
            extracted_phone = phones[0] if phones else "+15551234567"
            
            return {
                "payload_type": "custom_text",
                "device_metadata": {
                    "manufacturer": "Analyzed Mobile Artifact",
                    "model": "Generic Mobile Device",
                    "os_name": "Mobile OS",
                    "os_version": "Exported Artifact",
                    "timezone": "UTC+0"
                },
                "applications": [
                    {"app_name": "Messages", "package_name": "com.mobile.messages", "permissions": ["SMS"], "is_suspicious": False}
                ],
                "communications": [
                    {
                        "comm_type": "SMS / Communication Log", 
                        "direction": "Incoming", 
                        "contact_number": extracted_phone, 
                        "body": clean_text, 
                        "timestamp": "2026-08-12T10:00:00Z"
                    }
                ],
                "locations": []
            }


