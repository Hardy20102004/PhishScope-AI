import structlog
from sqlalchemy.orm import Session
from app.models.model_manager import RoutingPolicy, AIModel
from app.schemas.model_manager import RoutingResponse

logger = structlog.get_logger("phoenix.model_manager.router")

class RoutingEngine:
    """
    Selects the optimal model for a given task capability, handling fallbacks automatically.
    """
    def __init__(self, db: Session):
        self.db = db
        
    def get_model_for_task(self, capability: str) -> RoutingResponse:
        logger.info("routing_request", capability=capability)
        
        policy = self.db.query(RoutingPolicy).filter_by(capability=capability, is_active=True).first()
        if not policy:
            logger.error("no_active_routing_policy", capability=capability)
            raise ValueError(f"No active routing policy for capability: {capability}")
            
        primary: AIModel = policy.primary_model
        fallback: AIModel = policy.fallback_model
        
        if primary and primary.is_active and primary.provider.is_active and primary.health_status == "HEALTHY":
            logger.info("routing_to_primary", model_id=primary.id, name=primary.name)
            return RoutingResponse(model=primary, is_fallback=False)
            
        if fallback and fallback.is_active and fallback.provider.is_active and fallback.health_status == "HEALTHY":
            logger.warning("primary_unavailable_routing_to_fallback", primary_id=primary.id if primary else "None", fallback_id=fallback.id)
            return RoutingResponse(model=fallback, is_fallback=True)
            
        logger.error("no_models_available", capability=capability)
        raise ValueError(f"No healthy models available to handle capability: {capability}")
