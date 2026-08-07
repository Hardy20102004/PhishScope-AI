from typing import Any, Dict, List


class FormAnalysisEngine:
    """
    Inspects form targets, hidden inputs, and potential phishing vectors (e.g., login or credit card forms).
    """
    
    @staticmethod
    def analyze(forms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for form in forms:
            action = form.get("action", "")
            inputs = form.get("inputs", [])
            
            is_login = False
            has_password = False
            has_credit_card = False
            requests_personal_info = False
            is_hidden = False # Can't fully determine without computed CSS, but we check input types
            
            for inp in inputs:
                inp_type = inp.get("type", "").lower()
                inp_name = inp.get("name", "").lower()
                
                if inp_type == "password" or "password" in inp_name or "pass" in inp_name:
                    has_password = True
                    is_login = True
                    
                if "card" in inp_name or "cc" in inp_name or "cvv" in inp_name or "expiry" in inp_name:
                    has_credit_card = True
                    
                if "ssn" in inp_name or "dob" in inp_name or "phone" in inp_name:
                    requests_personal_info = True
                    
                if inp_type == "hidden":
                    is_hidden = True # Form has hidden inputs (very common, but tracked)
                    
            results.append({
                "action_url": action,
                "is_login": is_login,
                "has_password_field": has_password,
                "has_credit_card_field": has_credit_card,
                "requests_personal_info": requests_personal_info,
                "is_hidden": is_hidden
            })
            
        return results

class CookieAnalysisEngine:
    """
    Inspects Cookie configurations for security risks.
    """
    
    @staticmethod
    def analyze(cookies: List[Dict[str, Any]]) -> dict:
        # We just return the cookies, they are already structured by fetcher, 
        # but we could calculate a security score here.
        insecure_cookies = 0
        for cookie in cookies:
            if not cookie.get("secure") or not cookie.get("httponly"):
                insecure_cookies += 1
                
        return {
            "cookies": cookies,
            "insecure_count": insecure_cookies
        }
