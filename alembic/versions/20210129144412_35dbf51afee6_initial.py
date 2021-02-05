"""'initial'

Revision ID: 35dbf51afee6
Revises: 
Create Date: 2021-01-29 14:44:12.594927

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '35dbf51afee6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('host',
		sa.Column('host_id', sa.Integer(), autoincrement=True),
		sa.Column('domain', sa.String(length=128), nullable=False),
		sa.Column('added_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.Column('access_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.Column('times_offline', sa.SMALLINT(), nullable=False, server_default='0'),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.PrimaryKeyConstraint('host_id')
	)
	op.create_index(op.f('ix_host_domain'), 'host', ['domain'], unique=True)

	op.create_table('machine',
		sa.Column('machine_id', sa.Integer(), nullable=False),
		sa.Column('ip', postgresql.INET(), nullable=False),
		sa.Column('institute', sa.TEXT(), nullable=True),
		sa.Column('external', sa.Boolean(), nullable=False, server_default='false'),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.PrimaryKeyConstraint('machine_id')
	)
	op.create_index(op.f('ix_machine_ip'), 'machine', ['ip'], unique=True)
	
	op.create_table('path',
		sa.Column('path_id', sa.Integer(), nullable=False),
		sa.Column('host_id', sa.Integer(), nullable=False),
		sa.Column('url', sa.String(length=128), nullable=False),
		sa.Column('added_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.Column('access_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.Column('times_offline', sa.SMALLINT(), nullable=False, server_default='0'),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.ForeignKeyConstraint(['host_id'], ['host.host_id'], ),
		sa.PrimaryKeyConstraint('path_id')
	)
	op.create_index(op.f('ix_path_url'), 'path', ['url'], unique=True)
	
	op.create_table('machine_host',
		sa.Column('host_id', sa.Integer(), nullable=False),
		sa.Column('machine_id', sa.Integer(), nullable=False),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.ForeignKeyConstraint(['host_id'], ['host.host_id'], ),
		sa.ForeignKeyConstraint(['machine_id'], ['machine.machine_id'], ),
		sa.PrimaryKeyConstraint('host_id', 'machine_id')
	)


def downgrade():
	op.drop_table('machine_host')
	op.drop_index(op.f('ix_path_url'), table_name='path')
	op.drop_table('path')
	op.drop_index(op.f('ix_machine_ip'), table_name='machine')
	op.drop_table('machine')
	op.drop_index(op.f('ix_host_domain'), table_name='host')
	op.drop_table('host')
