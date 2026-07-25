import uuid
import structlog
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.models.multi_agent import MessageType

logger = structlog.get_logger("phoenix.multi_agent.communication")

class CommunicationBus:
    """
    Secure messaging backbone for multi-agent interoperability.
    Supports Point-to-Point (Handoff, Req/Resp) and Broadcast modes.
    """
    def __init__(self):
        self._message_ledger: List[Dict[str, Any]] = []
        self._subscribers: Dict[str, list] = {}

    def subscribe(self, agent_id: str, callback: callable):
        if agent_id not in self._subscribers:
            self._subscribers[agent_id] = []
        self._subscribers[agent_id].append(callback)
        logger.debug("agent_subscribed_to_bus", agent_id=agent_id)

    async def publish(self, sender_id: str, message_type: MessageType, content: Dict[str, Any], receiver_id: Optional[str] = None, correlation_id: Optional[str] = None) -> str:
        msg_id = str(uuid.uuid4())
        message = {
            "id": msg_id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message_type": message_type.value,
            "content": content,
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self._message_ledger.append(message)
        logger.info("message_published", msg_id=msg_id, type=message_type.value, sender=sender_id, receiver=receiver_id)
        
        # Dispatch to subscribers asynchronously
        if message_type == MessageType.BROADCAST:
            for agt_id, callbacks in self._subscribers.items():
                if agt_id != sender_id:
                    for cb in callbacks:
                        # In production this would use asyncio.create_task or a true message queue (Redis/RabbitMQ)
                        cb(message)
        elif receiver_id and receiver_id in self._subscribers:
            for cb in self._subscribers[receiver_id]:
                cb(message)
                
        return msg_id

    def get_messages_by_correlation(self, correlation_id: str) -> List[Dict[str, Any]]:
        return [m for m in self._message_ledger if m["correlation_id"] == correlation_id]

    def get_all_messages(self, limit: int = 100) -> List[Dict[str, Any]]:
        return list(reversed(self._message_ledger))[:limit]
