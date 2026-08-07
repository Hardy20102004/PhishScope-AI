"""add missing fk indexes for performance

Revision ID: fk_indexes_001
Revises: 92fce8da2f28
Create Date: 2026-07-27T11:04:12.295921

"""
from typing import Sequence, Union
from alembic import op

revision: str = 'fk_indexes_001'
down_revision: Union[str, None] = '96a008fb3aae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
