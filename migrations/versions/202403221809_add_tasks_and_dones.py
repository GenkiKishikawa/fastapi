"""Add tasks and dones

Revision ID: 8807b75e343e
Revises: 
Create Date: 2024-03-22 18:09:28.926478+09:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8807b75e343e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tasks',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tasks_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=1024), autoincrement=False, nullable=True),
    sa.Column('due_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='tasks_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('dones',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id'], ['tasks.id'], name='dones_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='dones_pkey')
    )


def downgrade() -> None:
    op.drop_table('dones')
    op.drop_table('tasks')
