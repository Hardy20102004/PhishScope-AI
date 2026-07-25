import json
import time
import uuid
from typing import Any, Dict, List, Optional

import structlog

from app.ai_brain.optimization import ContextCompressor
from app.models.ai_brain import MemoryTier

logger = structlog.get_logger("phoenix.ai_brain.memory")

class MemoryManager:
    """
    Multi-Tiered Enterprise Memory Manager supporting Session, Case, Conversation,
    Evidence, Organization, and User Preferences memory stores with TTL expiration and compression.
    """
    def __init__(self, default_ttl_seconds: int = 86400 * 7): # 7-day default TTL
        self.default_ttl = default_ttl_seconds
        # In-memory fast storage: tier -> key_id -> record
        self._stores: Dict[str, Dict[str, Dict[str, Any]]] = {
            MemoryTier.SESSION.value: {},
            MemoryTier.CASE.value: {},
            MemoryTier.CONVERSATION.value: {},
            MemoryTier.EVIDENCE.value: {},
            MemoryTier.ORGANIZATION.value: {},
            MemoryTier.USER_PREF.value: {},
        }

    def _get_tier_store(self, tier: MemoryTier) -> Dict[str, Dict[str, Any]]:
        return self._stores.setdefault(tier.value, {})

    def store_memory(
        self,
        tier: MemoryTier,
        key: str,
        data: Dict[str, Any],
        ttl_seconds: Optional[int] = None,
        tenant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        store = self._get_tier_store(tier)
        now = time.time()
        expiry = now + (ttl_seconds if ttl_seconds is not None else self.default_ttl)
        
        record = {
            "id": str(uuid.uuid4()),
            "tier": tier.value,
            "key": key,
            "data": data,
            "tenant_id": tenant_id or "global_soc_tier",
            "created_at": now,
            "expires_at": expiry,
            "is_compressed": False,
            "compressed_summary": None
        }
        store[key] = record
        logger.info("memory_record_stored", tier=tier.value, key=key, ttl=expiry - now)
        return record

    def retrieve_memory(self, tier: MemoryTier, key: str) -> Optional[Dict[str, Any]]:
        store = self._get_tier_store(tier)
        if key not in store:
            return None

        record = store[key]
        if time.time() > record["expires_at"]:
            logger.info("memory_expired_and_purged", tier=tier.value, key=key)
            del store[key]
            return None

        return record.get("data")

    def list_tier_memories(self, tier: MemoryTier, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        store = self._get_tier_store(tier)
        now = time.time()
        valid_records = []
        expired_keys = []
        
        for k, record in store.items():
            if now > record["expires_at"]:
                expired_keys.append(k)
            elif tenant_id is None or record.get("tenant_id") == tenant_id:
                valid_records.append(record)
                
        for k in expired_keys:
            del store[k]
            
        return valid_records

    def compress_tier_memory(self, tier: MemoryTier, key: str) -> bool:
        """Compresses bulky JSON memory records into concise summary strings to preserve system memory."""
        store = self._get_tier_store(tier)
        if key not in store:
            return False
            
        record = store[key]
        raw_json = json.dumps(record["data"], default=str)
        if len(raw_json) > 1000 and not record["is_compressed"]:
            compressed = ContextCompressor.compress_by_truncation(raw_json, max_characters=800)
            record["is_compressed"] = True
            record["compressed_summary"] = compressed
            # Reduce footprint of original data structure
            record["data"] = {"compressed": True, "summary_text": compressed}
            logger.info("memory_compressed_successfully", tier=tier.value, key=key)
            return True
        return False

    def purge_expired(self) -> int:
        now = time.time()
        purged = 0
        for tier_name, store in self._stores.items():
            keys = list(store.keys())
            for k in keys:
                if now > store[k]["expires_at"]:
                    del store[k]
                    purged += 1
        if purged > 0:
            logger.info("scheduled_memory_purge_complete", purged_count=purged)
        return purged


class ConversationManager:
    """
    Manages interactive analyst diagnostic dialogue sessions, automatic sliding-window context trimming,
    and turn-by-turn evidence anchoring.
    """
    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager
        self.max_turns_before_compression = 8

    def add_turn(self, session_id: str, role: str, content: str, citations: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        history = self.memory.retrieve_memory(MemoryTier.CONVERSATION, session_id) or {"turns": []}
        turns = history.get("turns", [])
        
        turns.append({
            "role": role.upper(),
            "content": content,
            "citations": citations or [],
            "timestamp": time.time()
        })

        # Sliding window compression if conversation exceeds turn threshold
        if len(turns) > self.max_turns_before_compression:
            oldest_turns = turns[:-6] # Retain latest 6 turns completely intact
            summary_parts = [f"{t['role']}: {t['content'][:150]}..." for t in oldest_turns]
            compressed_intro = {
                "role": "SYSTEM_MEMORY_SUMMARY",
                "content": "Prior diagnostic turns condensed: " + " | ".join(summary_parts),
                "citations": [],
                "timestamp": time.time()
            }
            turns = [compressed_intro] + turns[-6:]
            logger.info("conversation_history_compressed", session_id=session_id, remaining_turns=len(turns))

        history["turns"] = turns
        self.memory.store_memory(MemoryTier.CONVERSATION, session_id, history, ttl_seconds=86400 * 3) # 3-day conversation retention
        return turns

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        history = self.memory.retrieve_memory(MemoryTier.CONVERSATION, session_id)
        return history.get("turns", []) if history else []

    def format_history_for_prompt(self, session_id: str) -> str:
        turns = self.get_history(session_id)
        if not turns:
            return ""
        lines = ["### Active Conversation History:"]
        for t in turns:
            lines.append(f"[{t['role']}]: {t['content']}")
        return "\n".join(lines)
