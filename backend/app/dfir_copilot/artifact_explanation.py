from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.dfir_copilot import DfirResponseChunk

class ArtifactExplanationEngine:
    """
    Explains complex technical artifacts in plain English.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def explain_artifact(self, artifact_context: str) -> list[DfirResponseChunk]:
        # Mocking an explanation of a registry key
        chunks = [
            DfirResponseChunk(
                content="The artifact is a modification to the Windows Registry key `HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run`.",
                classification="OBSERVATION",
                citations=[{"id": "REG-112", "type": "REGISTRY_KEY"}]
            ),
            DfirResponseChunk(
                content="This specific registry key is evaluated by the Windows OS during user logon. Any executable listed here will be launched automatically.",
                classification="ASSESSMENT",
                citations=[]
            ),
            DfirResponseChunk(
                content="This is a classic technique (T1547.001) used by malware to establish persistence across system reboots.",
                classification="ASSESSMENT",
                citations=[]
            )
        ]
        return chunks
