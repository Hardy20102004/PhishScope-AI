import structlog
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.rag import KnowledgeAsset, DocumentChunk, KnowledgeAssetStatus
from app.rag.chunking import ChunkingEngine
from app.rag.embedding import EmbeddingService
import json

logger = structlog.get_logger("phoenix.rag.ingestion")

class DocumentParser:
    """Extracts raw text and metadata from files."""
    def parse(self, content: bytes, content_type: str) -> str:
        if content_type == "text/plain":
            return content.decode("utf-8")
        elif content_type == "application/json":
            data = json.loads(content.decode("utf-8"))
            return json.dumps(data, indent=2)
        elif content_type == "text/markdown":
            return content.decode("utf-8")
        else:
            # Fallback for unhandled types
            logger.warning("unsupported_content_type", content_type=content_type)
            return content.decode("utf-8", errors="ignore")

class DocumentIngestionEngine:
    def __init__(self, db: Session):
        self.db = db
        self.parser = DocumentParser()
        self.chunker = ChunkingEngine()
        self.embedder = EmbeddingService()

    def ingest(self, 
               title: str, 
               content: bytes, 
               content_type: str, 
               source_type: str, 
               tenant_id: str,
               author: str = "system") -> KnowledgeAsset:
        
        logger.info("starting_ingestion", title=title, source_type=source_type)
        
        # 1. Parse content
        extracted_text = self.parser.parse(content, content_type)
        
        # 2. Create Asset Record
        asset = KnowledgeAsset(
            title=title,
            source_type=source_type,
            tenant_id=tenant_id,
            author=author,
            status=KnowledgeAssetStatus.PROCESSING
        )
        self.db.add(asset)
        self.db.flush()
        
        # 3. Chunk Document
        chunks = self.chunker.chunk_fixed(extracted_text)
        
        # 4. Generate Embeddings and Save Chunks
        for idx, text_chunk in enumerate(chunks):
            embedding = self.embedder.generate_embedding(text_chunk)
            
            doc_chunk = DocumentChunk(
                asset_id=asset.id,
                chunk_index=idx,
                content=text_chunk,
                vector_embedding=embedding,
                metadata_json={"source": title}
            )
            self.db.add(doc_chunk)
            
        asset.status = KnowledgeAssetStatus.ACTIVE
        self.db.commit()
        self.db.refresh(asset)
        
        logger.info("ingestion_complete", asset_id=asset.id, chunk_count=len(chunks))
        return asset
