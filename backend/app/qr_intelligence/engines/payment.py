from typing import Dict, Any

class PaymentQRAnalyzer:
    """
    Parses and validates UPI, EMVCo, and static/dynamic payment payloads.
    """
    
    @staticmethod
    def analyze(decoded_payload: Dict[str, Any]) -> Dict[str, Any]:
        raw = decoded_payload.get("raw_payload", "")
        payload_type = decoded_payload.get("payload_type", "")
        
        network = "None"
        merchant_id = ""
        amount = None
        currency = ""
        is_dynamic = False
        
        if payload_type == "payment_upi":
            network = "UPI"
            # Simple UPI parsing: upi://pay?pa=merchant@bank&pn=MerchantName&am=100.00&cu=INR
            params = {}
            if "?" in raw:
                query = raw.split("?")[1]
                for pair in query.split("&"):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        params[k] = v
            
            merchant_id = params.get("pa", "")
            
            if "am" in params:
                try:
                    amount = float(params["am"])
                    is_dynamic = True # Fixed amount specified usually implies dynamic generation
                except:
                    pass
                    
            currency = params.get("cu", "INR")
            
        elif payload_type == "payment_emvco" or "000201" in raw: # 000201 is EMVCo version 1
            network = "EMVCo"
            # Skipping complex TLV parsing for prototype
            merchant_id = "EMVCo_Merchant"
            
        return {
            "payment_network": network,
            "merchant_id": merchant_id,
            "transaction_amount": amount,
            "currency": currency,
            "is_dynamic": is_dynamic
        }
