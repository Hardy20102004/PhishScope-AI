from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from app.ai_brain.memory import MemoryManager as BaseMemoryManager
from app.models.multi_agent import MemoryTierExt

logger = structlog.get_logger("phoenix.multi_agent.memory")

class SharedMemoryManager:
    """
    Extends AI Security Brain memory tiering to support Multi-Agent specific memory topologies:
    Working, Evidence, Conversation, Case, Organization, Temporary, Persistent.
    """
    def __init__(self, core_memory_manager: BaseMemoryManager):
        self.core = core_memory_manager
        self._local_cache: Dict[str, Dict[str, Any]] = {}

    def store_item(self, tier: MemoryTierExt, key: str, content: Dict[str, Any], tenant_id: str = "default", ttl_seconds: Optional[int] = None):
        """Stores a JSON artifact into a specific memory tier."""
        cache_key = f"{tenant_id}:{tier.value}:{key}"
        self._local_cache[cache_key] = {
            "content": content,
            "timestamp": datetime.utcnow()
        }
        logger.debug("memory_item_stored", tier=tier.value, key=key)
        
        # In a real environment, this syncs with the Database SharedMemoryItem table.

    def retrieve_item(self, tier: MemoryTierExt, key: str, tenant_id: str = "default") -> Optional[Dict[str, Any]]:
        cache_key = f"{tenant_id}:{tier.value}:{key}"
        record = self._local_cache.get(cache_key)
        if record:
            return record["content"]
        return None

    def search_tier(self, tier: MemoryTierExt, tenant_id: str = "default") -> List[Dict[str, Any]]:
        prefix = f"{tenant_id}:{tier.value}:"
        results = []
        for k, v in self._local_cache.items():
            if k.startswith(prefix):
                results.append({"key": k.split(":")[-1], "content": v["content"]})
        return results

    def clear_temporary_memory(self, tenant_id: str = "default"):
        """Purges WORKING and TEMPORARY tiers post-execution."""
        keys_to_delete = []
        for k in self._local_cache.keys():
            if k.startswith(f"{tenant_id}:{MemoryTierExt.WORKING.value}") or k.startswith(f"{tenant_id}:{MemoryTierExt.TEMPORARY.value}"):
                keys_to_delete.append(k)
        
        for k in keys_to_delete:
            del self._local_cache[k]
        logger.info("temporary_memory_cleared", tenant_id=tenant_id, items_purged=len(keys_to_delete))
