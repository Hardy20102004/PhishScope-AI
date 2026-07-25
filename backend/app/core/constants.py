from enum import Enum


class Roles(str, Enum):
    GUEST = "guest"
    USER = "user"
    ANALYST = "analyst"
    RESPONDER = "responder"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class RiskLevels(str, Enum):
    CLEAN = "clean"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"
    CRITICAL = "critical"

class InvestigationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
