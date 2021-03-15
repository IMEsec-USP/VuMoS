"""add sqlmap

Revision ID: b4d50f3f1bcf
Revises: bba37bac95b0
Create Date: 2021-03-15 14:37:16.465349

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b4d50f3f1bcf'
down_revision = 'bba37bac95b0'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('sqlmap',
		sa.Column('path', sa.Integer(), nullable=False),
		sa.Column('clean', sa.Boolean(), server_default=sa.text('false'), nullable=False),
		sa.Column('output', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), server_default=sa.text('to_timestamp(0)'), nullable=False),
		sa.ForeignKeyConstraint(['path'], ['path.path_id'], ondelete="CASCADE" ),
		sa.PrimaryKeyConstraint('path'),
		schema='scans'
	)
	op.create_index(op.f('ix_scans_sqlmap_updated_dttm'), 'sqlmap', ['updated_dttm'], unique=False, schema='scans')
	op.alter_column(
		table_name="path",
		column_name="vars",
		type_=postgresql.JSONB
	)


def downgrade():
	op.alter_column(
		table_name="path",
		column_name="vars",
		type_=postgresql.JSON
	)
	op.drop_index(op.f('ix_scans_sqlmap_updated_dttm'), table_name='sqlmap', schema='scans')
	op.drop_table('sqlmap', schema='scans')

