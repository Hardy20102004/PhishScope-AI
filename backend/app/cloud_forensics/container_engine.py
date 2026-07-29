import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cloud_forensics import ContainerMetadata

class ContainerEngine:
    """
    Simulates parsing Docker/Containerd inspect outputs to detect container escapes.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_containers(self, env_id: uuid.UUID) -> list[ContainerMetadata]:
        
        containers = [
            ContainerMetadata(
                env_id=env_id,
                container_id="a1b2c3d4e5f6",
                image_name="nginx:latest",
                is_privileged=False,
                mounts_host_root=False,
                mounts_docker_sock=False,
                config_dump={"Env": ["PATH=/usr/local/sbin"], "Cmd": ["nginx", "-g", "daemon off;"]},
                is_compromised=False
            ),
            ContainerMetadata(
                env_id=env_id,
                container_id="f6e5d4c3b2a1",
                image_name="alpine:latest",
                is_privileged=True, # Severely anomalous
                mounts_host_root=True, # Allows container escape
                mounts_docker_sock=False,
                config_dump={"Env": ["PATH=/bin"], "Cmd": ["/bin/sh", "-c", "chroot /host /bin/bash"]},
                is_compromised=True
            )
        ]
        
        for c in containers:
            self.db.add(c)
            
        await self.db.commit()
        return containers
