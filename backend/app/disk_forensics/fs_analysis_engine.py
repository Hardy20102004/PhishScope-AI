import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.disk_forensics import DiskPartition, ForensicArtifact

class FileSystemAnalysisEngine:
    """
    Simulates parsing volume structures (e.g. NTFS MFT, EXT4 Inodes) and extracting active file paths.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def parse_image(self, image_id: uuid.UUID) -> list[DiskPartition]:
        # Mocking the detection of an NTFS partition
        partition = DiskPartition(
            disk_image_id=image_id,
            partition_type="NTFS",
            start_sector=2048,
            size_bytes=50000000000 # 50 GB
        )
        self.db.add(partition)
        await self.db.commit()
        await self.db.refresh(partition)
        
        # Mocking the extraction of active files
        artifacts = [
            ForensicArtifact(partition_id=partition.id, filepath="C:\\Windows\\System32\\cmd.exe", is_deleted=False),
            ForensicArtifact(partition_id=partition.id, filepath="C:\\Users\\Admin\\Desktop\\passwords.txt", is_deleted=False),
            ForensicArtifact(partition_id=partition.id, filepath="C:\\Temp\\malware.exe", is_deleted=False)
        ]
        
        for a in artifacts:
            self.db.add(a)
            
        await self.db.commit()
        
        # Refresh to load relationships
        await self.db.refresh(partition, ["artifacts"])
        return [partition]
