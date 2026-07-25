import time
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.schemas.rag import (
    KnowledgeAssetResponse,
    RAGSearchRequest,
    RAGSearchResponse
)
from app.models.rag import KnowledgeAssetStatus, RAGAnalyticsLog
from app.rag.ingestion import DocumentIngestionEngine
from app.rag.retrieval import HybridRetrievalEngine
from app.rag.governance import KnowledgeManager
from app.rag.citation import CitationEngine

router = APIRouter()

@router.post("/ingest", response_model=KnowledgeAssetResponse)
async def ingest_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    source_type: str = Form("UPLOAD"),
    tenant_id: Optional[str] = Form(None),
    db: Session = Depends(deps.get_db)
):
    """Ingest a new document into the RAG Knowledge Platform."""
    content = await file.read()
    
    ingestion_engine = DocumentIngestionEngine(db)
    try:
        asset = ingestion_engine.ingest(
            title=title or file.filename,
            content=content,
            content_type=file.content_type,
            source_type=source_type,
            tenant_id=tenant_id
        )
        return asset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=RAGSearchResponse)
def search_knowledge(req: RAGSearchRequest, db: Session = Depends(deps.get_db)):
    """Execute a hybrid RAG search against the enterprise knowledge base."""
    start_time = time.time()
    
    retrieval_engine = HybridRetrievalEngine(db)
    
    try:
        results = retrieval_engine.search(
            query=req.query,
            top_k=req.top_k,
            search_type=req.search_type,
            tenant_id=req.tenant_id
        )
    except Exception as e:
        # Log failure
        db.add(RAGAnalyticsLog(query_text=req.query, search_type=req.search_type, latency_ms=0, results_count=0, success=False))
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))
        
    latency = (time.time() - start_time) * 1000
    
    # Log success
    db.add(RAGAnalyticsLog(
        query_text=req.query, 
        search_type=req.search_type, 
        latency_ms=latency, 
        results_count=len(results), 
        success=True
    ))
    db.commit()
    
    return RAGSearchResponse(
        query=req.query,
        results=results,
        latency_ms=latency
    )

@router.get("/assets", response_model=List[KnowledgeAssetResponse])
def list_assets(tenant_id: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    manager = KnowledgeManager(db)
    return manager.list_assets(tenant_id=tenant_id, skip=skip, limit=limit)

@router.put("/assets/{asset_id}/status", response_model=KnowledgeAssetResponse)
def update_asset_status(asset_id: str, status: str, db: Session = Depends(deps.get_db)):
    manager = KnowledgeManager(db)
    try:
        new_status = KnowledgeAssetStatus(status.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        
    asset = manager.update_status(asset_id, new_status)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
