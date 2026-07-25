import structlog
from sqlalchemy.orm import Session
from app.models.model_manager import AIProvider, AIModel
from app.schemas.model_manager import AIProviderCreate, AIModelCreate

logger = structlog.get_logger("phoenix.model_manager.registry")

class ModelRegistryService:
    def __init__(self, db: Session):
        self.db = db
        
    def register_provider(self, req: AIProviderCreate) -> AIProvider:
        logger.info("registering_provider", name=req.name)
        
        provider = AIProvider(
            name=req.name,
            base_url=req.base_url,
            api_key_secret=req.api_key_secret,
            is_active=req.is_active
        )
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(provider)
        return provider
        
    def register_model(self, req: AIModelCreate) -> AIModel:
        logger.info("registering_model", name=req.name, provider_id=req.provider_id)
        
        model = AIModel(
            provider_id=req.provider_id,
            name=req.name,
            version=req.version,
            capabilities=req.capabilities,
            context_window=req.context_window,
            cost_per_1k_prompt=req.cost_per_1k_prompt,
            cost_per_1k_completion=req.cost_per_1k_completion,
            is_active=req.is_active
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model
