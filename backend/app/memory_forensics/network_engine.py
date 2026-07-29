import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.memory_forensics import MemoryNetworkConnection

class NetworkEngine:
    """
    Simulates parsing the network socket structures (netscan) to extract active and listening connections.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def extract_connections(self, image_id: uuid.UUID) -> list[MemoryNetworkConnection]:
        # Mocking active connections extracted from RAM
        connections = [
            MemoryNetworkConnection(
                memory_image_id=image_id,
                pid=1408, # explorer.exe
                protocol="TCP",
                local_ip="192.168.1.100",
                local_port=49152,
                remote_ip="20.44.11.9", # Microsoft
                remote_port=443,
                state="ESTABLISHED"
            ),
            MemoryNetworkConnection(
                memory_image_id=image_id,
                pid=9091, # svchost.exe (the hidden malicious one)
                protocol="TCP",
                local_ip="192.168.1.100",
                local_port=55112,
                remote_ip="103.11.42.19", # Mock Malicious C2
                remote_port=4444,
                state="ESTABLISHED"
            ),
            MemoryNetworkConnection(
                memory_image_id=image_id,
                pid=4, # System
                protocol="TCP",
                local_ip="0.0.0.0",
                local_port=445,
                remote_ip="0.0.0.0",
                remote_port=0,
                state="LISTENING"
            )
        ]
        
        for c in connections:
            self.db.add(c)
            
        await self.db.commit()
        return connections
