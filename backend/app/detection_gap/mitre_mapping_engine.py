class MitreMappingEngine:
    """
    Provides structural dictionary/mapping of tactics to techniques used by the other engines.
    """
    TACTICS = {
        "TA0001": "Initial Access",
        "TA0002": "Execution",
        "TA0003": "Persistence",
        "TA0004": "Privilege Escalation",
        "TA0005": "Defense Evasion",
        "TA0006": "Credential Access",
        "TA0007": "Discovery",
        "TA0008": "Lateral Movement",
        "TA0009": "Collection",
        "TA0011": "Command and Control",
        "TA0010": "Exfiltration",
        "TA0040": "Impact"
    }
    
    @classmethod
    def get_tactic_name(cls, tactic_id: str) -> str:
        return cls.TACTICS.get(tactic_id, "Unknown Tactic")
