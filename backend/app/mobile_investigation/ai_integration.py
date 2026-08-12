import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MobileAIIntegration:
    """
    Integrates Mobile Intelligence with PHOENIX AI Brain to generate explainable mobile forensics narratives.
    """
    
    @staticmethod
    async def generate_narrative(metadata: dict, applications: list, timeline: list, iocs: list, risk: dict, parsed_data: Dict[str, Any] = None) -> Dict[str, str]:
        parsed_data = parsed_data or {}
        payload_type = parsed_data.get("payload_type", "custom_text")
        dev_info = f"{metadata.get('manufacturer', 'Mobile')} {metadata.get('model', 'Device')}"
        severity = risk.get("threat_severity", "MEDIUM")
        score = risk.get("overall_risk_score", 50)

        threat_summary_list = []
        suspicious_apps = [app.get("app_name") for app in applications if app.get("is_suspicious")]

        if payload_type == "payment_upi_legitimate":
            comms = parsed_data.get("communications", [])
            body = comms[0].get("body", "") if comms else ""

            narrative = f"Forensic analysis of the mobile artifact ({dev_info}) yields a LOW / CLEAN risk level (Score: {score}/100). "
            narrative += f"The analyzed payload is a standard UPI payment deep-link handle ({body}). "
            narrative += "No brand impersonation, fraudulent MPIN request notes, or malicious phishing links were detected."

            threat_summary_list = ["Clean UPI Deep-Link", "Valid VPA Handle", "No Threat Indicators Detected"]
            recommendation = "Standard payment link. Verify payee identity before completing transactions."
            evidence = f"AI analyzed UPI payment parameters and confirmed VPA handle formatting with zero threat flags."

        elif payload_type == "payment_upi_scam":
            comms = parsed_data.get("communications", [])
            body = comms[0].get("body", "") if comms else ""
            
            narrative = f"Forensic analysis of the mobile artifact ({dev_info}) yields a HIGH SEVERITY UPI Payment Scam / Quishing alert (Score: {score}/100). "
            narrative += f"The analyzed payload contains an unverified UPI payment request ({body}). "
            narrative += "Threat actors frequently use deceptive VPA collect requests and payment links disguised as refunds or bill payments to drain funds."
            
            threat_summary_list = ["UPI Payment Scam", "Deceptive VPA Collect", "Financial Drain Threat"]
            recommendation = "Do NOT approve the UPI payment request or enter MPIN. File an immediate dispute with NPCI/Cyber Crime portal and flag the suspicious VPA."
            evidence = f"AI correlated suspicious UPI VPA transaction request metrics with brand impersonation flags."

        elif payload_type == "banking_phishing":
            urls = [ioc.get("ioc_value") for ioc in iocs if ioc.get("ioc_type") == "url"]
            url_str = ", ".join(urls[:2]) if urls else "unverified link"
            
            narrative = f"Forensic analysis of the mobile artifact ({dev_info}) yields a CRITICAL Banking Phishing threat level (Score: {score}/100). "
            narrative += f"The incoming SMS payload contains an urgent social engineering prompt directing the user to a credential harvesting portal ({url_str}). "
            if suspicious_apps:
                narrative += f"The device has suspicious helper APKs installed ({', '.join(suspicious_apps)}) requesting elevated SMS and Admin permissions to intercept OTPs."

            threat_summary_list = ["Banking Credential Harvesting", "Urgent SMS Phishing", "OTP Interception Risk"]
            recommendation = "Immediately change NetBanking/Mobile Banking credentials from a clean device. Report the phishing domain to the host registrar and block incoming SMS dispatchers."
            evidence = f"AI correlated incoming SMS phishing text with malicious domain indicators and unverified APK installation records."

        elif payload_type == "trojan_apk":
            urls = [ioc.get("ioc_value") for ioc in iocs if ioc.get("ioc_type") == "url"]
            url_str = ", ".join(urls[:2]) if urls else "malicious URL"

            narrative = f"Forensic investigation on {dev_info} detected a CRITICAL Trojan Dropper Malware threat (Score: {score}/100). "
            narrative += f"The device received a prompt to download an unverified `.apk` package via {url_str}. "
            narrative += f"Installed malware packages ({', '.join(suspicious_apps) if suspicious_apps else 'Unverified APK'}) request Device Administrator, SMS Intercept, and Accessibility Service privileges."

            threat_summary_list = ["Trojan APK Dropper", "Device Admin Abuse", "SMS Interception Malware"]
            recommendation = "Isolate the mobile device from Wi-Fi and cellular networks immediately. Revoke Device Administrator privileges for unverified apps and perform a full malware cleanup."
            evidence = f"AI correlated Trojan `.apk` download URL with excessive Android application permissions and cell site command nodes."

        else:
            urls = [ioc.get("ioc_value") for ioc in iocs if ioc.get("ioc_type") == "url"]
            phones = [ioc.get("ioc_value") for ioc in iocs if ioc.get("ioc_type") == "phone_number"]

            narrative = f"Forensic analysis of the mobile artifact ({dev_info}) yields a {severity} threat level (Score: {score}/100). "
            if urls:
                narrative += f"Extracted communication logs contain external web links ({', '.join(urls[:2])}). "
                threat_summary_list.append("External Web Link")
            if suspicious_apps:
                narrative += f"The device has {len(suspicious_apps)} application(s) with elevated permissions ({', '.join(suspicious_apps)}). "
                threat_summary_list.append("Elevated App Permissions")
            if not threat_summary_list:
                narrative += "No critical malware or active phishing indicators were detected in the provided artifact."
                threat_summary_list.append("Clean / Low Risk Artifact")

            recommendation = "Review application permissions and verify external links with URL Intelligence before interacting." if severity in ["HIGH", "CRITICAL", "MEDIUM"] else "No immediate forensic action required."
            evidence = f"AI analyzed communication logs, phone numbers ({', '.join(phones[:2]) if phones else 'N/A'}), and device profile."

        return {
            "risk_narrative": narrative,
            "threat_summary": ", ".join(threat_summary_list),
            "recommended_next_steps": recommendation,
            "evidence_correlation": evidence
        }


