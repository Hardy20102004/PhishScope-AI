import hashlib
import structlog
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.ai_context import ContextCacheEntry

logger = structlog.get_logger("phoenix.ai_context.caching")

class ContextCache:
    """
    Hybrid cache for Semantic Segments and fully built prompts.
    In production, this would use Redis for fast lookups. We use the DB for simplicity here.
    """
    def __init__(self, db: Session):
        self.db = db

    def generate_key(self, query: str, investigation_id: Optional[str] = None) -> str:
        """Deterministically generate a cache key based on the core inputs."""
        raw = f"{query}_{investigation_id or 'none'}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    def get_cached_context(self, cache_key: str) -> Optional[ContextCacheEntry]:
        entry = self.db.query(ContextCacheEntry).filter(
            ContextCacheEntry.cache_key == cache_key,
            ContextCacheEntry.expires_at > datetime.utcnow()
        ).first()
        
        if entry:
            logger.info("context_cache_hit", cache_key=cache_key)
        else:
            logger.debug("context_cache_miss", cache_key=cache_key)
            
        return entry

    def set_cached_context(self, cache_key: str, assembled_context: str, token_count: int, ttl_minutes: int = 60):
        expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
        
        # Upsert logic
        entry = self.db.query(ContextCacheEntry).filter(ContextCacheEntry.cache_key == cache_key).first()
        if entry:
            entry.assembled_context = assembled_context
            entry.token_count = token_count
            entry.expires_at = expires_at
        else:
            entry = ContextCacheEntry(
                cache_key=cache_key,
                assembled_context=assembled_context,
                token_count=token_count,
                expires_at=expires_at
            )
            self.db.add(entry)
            
        self.db.commit()
        logger.debug("context_cache_set", cache_key=cache_key)
