
class BrandProtectionEngine:
    """
    Detects Typosquatting, Homograph Attacks, and Brand Impersonation.
    """
    
    KNOWN_BRANDS = [
        "microsoft", "apple", "google", "amazon", "netflix",
        "paypal", "chase", "bankofamerica", "wellsfargo"
    ]
    
    @classmethod
    def analyze(cls, hostname: str, root_domain: str) -> dict:
        if not root_domain:
            return {}
            
        is_homograph = cls._detect_homograph(hostname)
        
        # Simple typosquatting detection (Levenshtein distance could be used here)
        # For this prototype, we check if a known brand is a substring but not the exact root domain
        # or if the root domain is very similar.
        
        is_typosquat = False
        targeted_brand = None
        impersonation_score = 0.0
        
        domain_without_suffix = root_domain.split('.')[0] if '.' in root_domain else root_domain
        
        for brand in cls.KNOWN_BRANDS:
            if brand == domain_without_suffix:
                # Legitimate brand (or exact match)
                pass
            elif brand in domain_without_suffix:
                is_typosquat = True
                targeted_brand = brand
                impersonation_score = 0.8
                break
            elif cls._levenshtein(brand, domain_without_suffix) <= 2:
                is_typosquat = True
                targeted_brand = brand
                impersonation_score = 0.9
                break
                
        return {
            "is_typosquat": is_typosquat,
            "typosquat_target": targeted_brand if is_typosquat else None,
            "is_homograph": is_homograph,
            "homograph_target": None, # Complex to determine without AI
            "brand_impersonation_score": impersonation_score,
            "targeted_brand": targeted_brand
        }
        
    @staticmethod
    def _detect_homograph(hostname: str) -> bool:
        # Check for punycode which is often used in homograph attacks
        if "xn--" in hostname:
            return True
        # Check for mixed scripts or non-ASCII
        if any(ord(char) > 127 for char in hostname):
            return True
        return False
        
    @staticmethod
    def _levenshtein(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return BrandProtectionEngine._levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
