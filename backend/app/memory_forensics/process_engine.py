import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.memory_forensics import MemoryProcess

class ProcessEngine:
    """
    Simulates parsing the EPROCESS structure (pslist) and cross-referencing thread lists (psxview) to find hidden processes.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def extract_processes(self, image_id: uuid.UUID) -> list[MemoryProcess]:
        # Mocking process extraction and unlinked process detection (DKOM)
        processes = [
            MemoryProcess(memory_image_id=image_id, pid=4, ppid=0, name="System", is_hidden=False),
            MemoryProcess(memory_image_id=image_id, pid=342, ppid=4, name="smss.exe", is_hidden=False),
            MemoryProcess(memory_image_id=image_id, pid=612, ppid=342, name="csrss.exe", is_hidden=False),
            MemoryProcess(memory_image_id=image_id, pid=1408, ppid=612, name="explorer.exe", is_hidden=False),
            # Anomalous / Hidden
            MemoryProcess(memory_image_id=image_id, pid=4912, ppid=1408, name="cmd.exe", is_hidden=False),
            MemoryProcess(memory_image_id=image_id, pid=9091, ppid=4912, name="svchost.exe", is_hidden=True, is_injected=True) # Fake svchost, unlinked
        ]
        
        for p in processes:
            self.db.add(p)
            
        await self.db.commit()
        return processes
