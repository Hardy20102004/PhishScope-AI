import time

import structlog
from sqlalchemy.orm import Session

from app.ai_context.caching import ContextCache
from app.ai_context.compression import ContextCompressionEngine
from app.ai_context.ranking import ContextRankingEngine
from app.ai_context.validation import ContextPolicyEngine, ContextValidator
from app.ai_memory.search import HybridSearchEngine
from app.models.ai_context import ContextAuditLog
from app.schemas.ai_context import ContextRequest, ContextResponse, OptimizationMetrics

logger = structlog.get_logger("phoenix.ai_context.builder")

class ContextBuilder:
    """
    Orchestrates the retrieval of data from the Memory Engine.
    """
    def __init__(self, db: Session):
        self.search_engine = HybridSearchEngine(db)
        self.ranking = ContextRankingEngine()

    def fetch_raw_context(self, request: ContextRequest) -> str:
        """
        Retrieves matching memories and builds the initial unoptimized block.
        """
        filters = {}
        if request.investigation_id:
            filters["investigation_id"] = request.investigation_id
            
        memories = self.search_engine.search(
            query_text=request.query,
            semantic=True if request.query else False,
            filters=filters,
            limit=15
        )
        
        ranked_memories = self.ranking.rank_memories(memories, request.query or "")
        
        blocks = []
        for m in ranked_memories:
            blocks.append(f"[{m.memory_type} | {m.security_classification}] {m.title}\n{m.description}")
            
        return "\n\n".join(blocks)

class ContextManager:
    """
    The facade for generating AI Context. 
    Coordinates fetching, compressing, policy enforcement, and caching.
    """
    def __init__(self, db: Session):
        self.db = db
        self.builder = ContextBuilder(db)
        self.cache = ContextCache(db)
        self.compression = ContextCompressionEngine()
        self.policy = ContextPolicyEngine(db)
        self.validator = ContextValidator()

    def build_context(self, request: ContextRequest) -> ContextResponse:
        start_time = time.time()
        
        # 1. Check Cache
        cache_key = self.cache.generate_key(request.query or "", request.investigation_id)
        cached = self.cache.get_cached_context(cache_key)
        
        if cached:
            latency = (time.time() - start_time) * 1000
            metrics = OptimizationMetrics(
                original_tokens=cached.token_count,
                compressed_tokens=cached.token_count,
                compression_ratio=1.0,
                build_latency_ms=latency,
                cache_hit=True
            )
            # We assume cached items have already passed validation
            val_res = self.validator.validate(cached.assembled_context, cached.token_count)
            return ContextResponse(
                assembled_context=cached.assembled_context,
                metrics=metrics,
                validation=val_res
            )
            
        # 2. Build Raw Context
        raw_text = self.builder.fetch_raw_context(request)
        if not raw_text:
            raw_text = "No relevant context found."
            
        # 3. Apply Policies (e.g. PII masking)
        redacted_text, warnings = self.policy.apply_policies(raw_text)
        
        # 4. Compress & Optimize
        compressed_text = redacted_text
        orig_tokens = self.compression.estimate_tokens(redacted_text)
        comp_tokens = orig_tokens
        
        if request.apply_compression:
            compressed_text, orig_tokens, comp_tokens = self.compression.compress(redacted_text, request.max_tokens)
            
        # 5. Final Validation
        val_res = self.validator.validate(compressed_text, comp_tokens)
        val_res.warnings.extend(warnings)
        
        # 6. Cache Result
        if val_res.is_valid:
            self.cache.set_cached_context(cache_key, compressed_text, comp_tokens)
            
        # 7. Audit Log
        latency = (time.time() - start_time) * 1000
        audit = ContextAuditLog(
            investigation_id=request.investigation_id,
            actor_id=request.actor_id,
            action="BUILD",
            original_tokens=orig_tokens,
            compressed_tokens=comp_tokens,
            build_latency_ms=latency
        )
        self.db.add(audit)
        self.db.commit()
        
        metrics = OptimizationMetrics(
            original_tokens=orig_tokens,
            compressed_tokens=comp_tokens,
            compression_ratio=orig_tokens / max(1, comp_tokens),
            build_latency_ms=latency,
            cache_hit=False
        )
        
        return ContextResponse(
            assembled_context=compressed_text,
            metrics=metrics,
            validation=val_res
        )
