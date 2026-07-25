from typing import List

import structlog

from app.models.ai_memory import MemoryItem

logger = structlog.get_logger("phoenix.ai_context.ranking")

class ContextRankingEngine:
    """
    Ranks evidence and memory based on relevance, freshness, and threat severity.
    """
    def __init__(self):
        pass

    def rank_memories(self, memories: List[MemoryItem], query: str = "") -> List[MemoryItem]:
        """
        Sorts the provided memories.
        In a real implementation, this would use a cross-encoder model for re-ranking.
        Here we mock the ranking by relying on existing confidence scores and type priority.
        """
        def get_priority(mem: MemoryItem) -> float:
            base = mem.confidence_score or 1.0
            
            # Threat Intel is usually most critical
            if mem.memory_type == "THREAT_INTEL":
                base += 0.5
            elif mem.memory_type == "WORKING":
                base += 0.2
                
            # Keyword match bonus
            if query and query.lower() in mem.title.lower():
                base += 0.3
                
            return base

        # Sort descending by calculated priority
        sorted_memories = sorted(memories, key=get_priority, reverse=True)
        logger.debug("memories_ranked", count=len(sorted_memories))
        return sorted_memories
