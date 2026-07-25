import structlog
from sqlalchemy.orm import Session

from app.models.model_manager import AIModel, ModelCostLog

logger = structlog.get_logger("phoenix.model_manager.cost")

class CostManager:
    """
    Calculates and logs the financial cost of an AI interaction.
    """
    def __init__(self, db: Session):
        self.db = db
        
    def log_usage(self, model_id: str, task_type: str, prompt_tokens: int, completion_tokens: int, tenant_id: str = None) -> ModelCostLog:
        model = self.db.query(AIModel).filter_by(id=model_id).first()
        if not model:
            raise ValueError("Model not found")
            
        # Calculate cost
        prompt_cost = (prompt_tokens / 1000.0) * model.cost_per_1k_prompt
        completion_cost = (completion_tokens / 1000.0) * model.cost_per_1k_completion
        total = prompt_cost + completion_cost
        
        log = ModelCostLog(
            tenant_id=tenant_id,
            model_id=model_id,
            task_type=task_type,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_cost=total
        )
        
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        
        logger.info("logged_model_cost", model=model.name, total_cost=total)
        return log
