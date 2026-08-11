"""
brand.py — Brand Protection Engine
Detects Typosquatting, Homograph Attacks, and Brand Impersonation.

Updated (v2):
- Added Indian banks, UPI, and government portals critical for UP Police Cyber Cell
- Improved typosquatting detection logic (more precise false positive avoidance)
"""


class BrandProtectionEngine:
    """
    Detects Typosquatting, Homograph Attacks, and Brand Impersonation.
    
    Brand list specifically tuned for UP Police Cyber Cell threats:
    - Major Indian banks (SBI, HDFC, ICICI, Paytm, etc.)
    - UPI/payment platforms
    - Government portals (.gov.in targets)
    - Global brands commonly spoofed in India
    """
    
    KNOWN_BRANDS = [
        # === Global Tech / Social ===
        "microsoft", "apple", "google", "amazon", "netflix",
        "paypal", "facebook", "instagram", "whatsapp", "twitter",
        "linkedin", "dropbox", "adobe",
        
        # === Indian Banks — HIGH PRIORITY for UP Police ===
        "sbi", "statebankofindia", "hdfcbank", "hdfc", "icicibank",
        "icici", "axisbank", "axis", "kotakbank", "kotak",
        "pnb", "punjabbank", "bankofbaroda", "canarabank",
        "unionbank", "indusindbank", "yesbank", "idfcbank",
        
        # === UPI / Payment Platforms — Common Scam Targets ===
        "paytm", "phonepe", "gpay", "googlepay", "bhimupi",
        "bhim", "amazonpay", "mobikwik", "freecharge",
        "razorpay", "cashfree",
        
        # === Indian Government Portals — CRITICAL for UP Police ===
        "incometax", "epfindia", "irctc", "aadhaar", "uidai",
        "digilocker", "mygov", "umang", "nicin", "gov",
        "uppolice", "upgovt",
        
        # === E-Commerce ===
        "flipkart", "meesho", "snapdeal", "myntra", "nykaa",
        "bigbasket", "zomato", "swiggy",
        
        # === US Banks ===
        "chase", "bankofamerica", "wellsfargo", "citibank",
    ]
    
    # Short brands that could cause false positives if substring-matched aggressively
    # These will only be matched with Levenshtein, not substring
    SHORT_BRANDS_SUBSTRING_EXCLUDED = {"sbi", "pnb", "gov", "nic", "hdfc", "axis"}
    
    @classmethod
    def analyze(cls, hostname: str, root_domain: str) -> dict:
        if not root_domain:
            return {
                "is_typosquat": False,
                "typosquat_target": None,
                "is_homograph": False,
                "homograph_target": None,
                "brand_impersonation_score": 0.0,
                "targeted_brand": None,
            }
            
        is_homograph = cls._detect_homograph(hostname)
        
        is_typosquat = False
        targeted_brand = None
        impersonation_score = 0.0
        
        # Extract just the domain label (without TLD) for comparison
        domain_label = root_domain.split('.')[0] if '.' in root_domain else root_domain
        domain_label_lower = domain_label.lower()
        
        for brand in cls.KNOWN_BRANDS:
            # Exact match = legitimate brand (not a typosquat)
            if brand == domain_label_lower:
                break
            
            # Substring match: brand name is embedded in a longer domain
            # e.g. "sbisecurelogin.com" → contains "sbi" → typosquatting SBI
            # For short brands, require the domain to be significantly longer (not just brand + TLD)
            if brand in domain_label_lower:
                if brand in cls.SHORT_BRANDS_SUBSTRING_EXCLUDED:
                    # Only flag if domain is meaningfully longer than just the brand
                    # e.g. "sbisecure" (len 9 > sbi len 3 + 2) → flag it
                    if len(domain_label_lower) > len(brand) + 2:
                        is_typosquat = True
                        targeted_brand = brand
                        impersonation_score = 0.85
                        break
                else:
                    is_typosquat = True
                    targeted_brand = brand
                    impersonation_score = 0.85
                    break
            
            # Levenshtein distance — catches character substitutions like "paypa1.com"
            lev = cls._levenshtein(brand, domain_label_lower)
            if lev <= 2 and abs(len(brand) - len(domain_label_lower)) <= 3:
                is_typosquat = True
                targeted_brand = brand
                # Higher score for closer (1-edit) matches
                impersonation_score = 0.95 if lev == 1 else 0.85
                break
                
        return {
            "is_typosquat": is_typosquat,
            "typosquat_target": targeted_brand if is_typosquat else None,
            "is_homograph": is_homograph,
            "homograph_target": None,  # Requires AI to determine exact target
            "brand_impersonation_score": impersonation_score,
            "targeted_brand": targeted_brand,
        }
        
    @staticmethod
    def _detect_homograph(hostname: str) -> bool:
        """
        Detects homograph attacks using punycode and Unicode script analysis.
        Homograph attacks use visually similar Unicode chars (e.g., Cyrillic 'а' ≈ Latin 'a').
        """
        # Punycode is used to encode international domain names (xn-- prefix)
        if "xn--" in hostname:
            return True
        # Mixed or non-ASCII characters in hostname
        if any(ord(char) > 127 for char in hostname):
            return True
        return False
        
    @staticmethod
    def _levenshtein(s1: str, s2: str) -> int:
        """
        Computes Levenshtein edit distance between two strings.
        Used to detect typosquatting variants like 'gogle', 'amazoon', 'paypa1'.
        """
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
