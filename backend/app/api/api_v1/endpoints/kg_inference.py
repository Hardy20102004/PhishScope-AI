from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.knowledge_graph.inference import InferenceEngine

router = APIRouter()

@router.post("/run")
def run_inferences(db: Session = Depends(deps.get_db)):
    """
    Manually triggers the inference engine to deduce new relationships.
    In production, this runs as a background worker.
    """
    engine = InferenceEngine(db)
    engine.run_all_inferences()
    return {"status": "success", "message": "Inference engine completed successfully."}
