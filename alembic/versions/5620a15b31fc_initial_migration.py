"""initial migration

Revision ID: 5620a15b31fc
Revises: 
Create Date: 2026-04-26 22:13:53.241529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5620a15b31fc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear el tipo enum primero
    appointmentstatus = sa.Enum('pending', 'confirmed', 'completed', 'cancelled', name='appointmentstatus')
    appointmentstatus.create(op.get_bind(), checkfirst=True)
    
    # Convertir la columna con USING
    op.execute("ALTER TABLE appointments ALTER COLUMN status TYPE appointmentstatus USING status::appointmentstatus")

def downgrade() -> None:
    # Revertir a VARCHAR
    op.execute("ALTER TABLE appointments ALTER COLUMN status TYPE VARCHAR")
    
    # Eliminar el tipo enum
    sa.Enum(name='appointmentstatus').drop(op.get_bind(), checkfirst=True)
