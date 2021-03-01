"""add config and nmap

Revision ID: 444c7f1a4166
Revises: d13f5a4d0eca
Create Date: 2021-03-01 13:43:40.429649

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '444c7f1a4166'
down_revision = 'd13f5a4d0eca'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('config',
		sa.Column('config_id', sa.Integer(), nullable=False),
		sa.Column('name', sa.TEXT(), nullable=False),
		sa.Column('config', postgresql.JSON(astext_type=sa.Text()), server_default='{}', nullable=False),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
		sa.PrimaryKeyConstraint('config_id')
	)
	op.create_index(op.f('ix_config_name'), 'config', ['name'], unique=True)
	op.execute("""
		CREATE TRIGGER host_audit
		AFTER INSERT OR UPDATE OR DELETE ON config
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")

	op.create_table('nmap',
		sa.Column('machine_id', sa.Integer(), nullable=False),
		sa.Column('output', postgresql.JSON(astext_type=sa.Text()), nullable=True),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), server_default=sa.text('to_timestamp(0)'), nullable=False),
		sa.ForeignKeyConstraint(['machine_id'], ['machine.machine_id'], ),
		sa.PrimaryKeyConstraint('machine_id')
	)
	op.execute("""
		CREATE TRIGGER host_audit
		AFTER INSERT OR UPDATE OR DELETE ON nmap
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")

	op.add_column('machine', sa.Column('added_dttm', postgresql.TIMESTAMP(), server_default='now()', nullable=False))


def downgrade():
	op.drop_column('machine', 'added_dttm')
	op.drop_table('nmap')
	op.drop_table('config')
