"""empty message

Revision ID: 23cc747a113a
Revises: 279f8d753529
Create Date: 2025-09-09 11:16:02.682022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23cc747a113a'
down_revision = '279f8d753529'
branch_labels = None
depends_on = None

def upgrade():
    
    op.create_table('workspaces_imagery',
    sa.Column('workspace_id', sa.Integer(), nullable=False),
    sa.Column('definition', sa.Unicode(), nullable=False),
    sa.Column('modifiedAt', sa.DateTime(), nullable=False),
    sa.Column('modifiedBy', sa.UUID(), nullable=False),
    sa.Column('modifiedByName', sa.Unicode(), nullable=False),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ),
    sa.PrimaryKeyConstraint('workspace_id')
    )
    
    with op.batch_alter_table('workspaces', schema=None) as batch_op:
        batch_op.drop_column('imageryList')
    
    op.execute("""
        ALTER TABLE workspaces_imagery
        ALTER COLUMN definition
        TYPE JSON
        USING definition::json
    """)
    
    op.execute("""
        ALTER TABLE workspaces_long_quests
        ALTER COLUMN definition
        TYPE JSON
        USING definition::json
    """)


def downgrade():
    
    with op.batch_alter_table('workspaces', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imageryList', sa.VARCHAR(), autoincrement=False, nullable=True))

    op.drop_table('workspaces_imagery')
    
    op.execute("""
        ALTER TABLE workspaces_imagery
        ALTER COLUMN definition
        TYPE VARCHAR
        USING definition::text
    """)
    
    op.execute("""
        ALTER TABLE workspaces_long_quests
        ALTER COLUMN definition
        TYPE VARCHAR
        USING definition::text
    """)