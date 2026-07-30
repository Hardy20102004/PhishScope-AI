from sqlalchemy.orm import Session

from app.services.cyber_os.registry import RegistryService
from app.services.cyber_os.observability import ObservabilityService

class CyberOSKernel:
    """
    Central orchestration bus for the Enterprise Cyber Operating System.
    """
    def __init__(self, db: Session):
        self.db = db
        self.registry = RegistryService(db)
        self.observability = ObservabilityService(db)

    def get_kernel_overview(self) -> dict:
        modules = self.registry.get_registered_modules()
        
        return {
            "kernel_status": "ONLINE",
            "registered_modules_count": len(modules),
            "global_cpu_usage": 18.5,
            "global_memory_usage": 42.1,
            "active_alerts": 0,
            "ai_status": "ONLINE - UNIFIED BRAIN ACTIVE"
        }
