"""adding vunerability

Revision ID: d13f5a4d0eca
Revises: 35dbf51afee6
Create Date: 2021-02-12 14:35:16.996057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd13f5a4d0eca'
down_revision = '35dbf51afee6'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('vulnerability_type',
		sa.Column('vulnerability_type_id', sa.Integer(), nullable=False),
		sa.Column('name', sa.TEXT(), nullable=False),
		sa.Column('description', sa.TEXT(), nullable=True),
		sa.Column('severity', sa.SMALLINT(), nullable=False),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), server_default='now()', nullable=False),
		sa.PrimaryKeyConstraint('vulnerability_type_id')
	)
	op.create_index(op.f('ix_vulnerability_type_name'), 'vulnerability_type', ['name'], unique=True)
	op.create_index(op.f('ix_vulnerability_type_severity'), 'vulnerability_type', ['severity'], unique=False)
	op.execute("""
		CREATE TRIGGER host_audit
		AFTER INSERT OR UPDATE OR DELETE ON vulnerability_type
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")

	op.create_table('vulnerability',
		sa.Column('vulnerability_id', sa.Integer(), nullable=False),
		sa.Column('vulnerability_type_id', sa.Integer(), nullable=False),
		sa.Column('status', sa.Enum('found', 'confirmed', 'solved', 'false positive', name='vulnerability_status_enum'), nullable=False),
		sa.Column('found_by', sa.TEXT(), nullable=False),
		sa.Column('found_dttm', postgresql.TIMESTAMP(), server_default='now()', nullable=False),
		sa.Column('confirmed_by', sa.TEXT(), nullable=True),
		sa.Column('confirmed_dttm', postgresql.TIMESTAMP(), nullable=True),
		sa.Column('solved_dttm', postgresql.TIMESTAMP(), nullable=True),
		sa.Column('host_id', sa.Integer(), nullable=True),
		sa.Column('path_id', sa.Integer(), nullable=True),
		sa.Column('machine_id', sa.Integer(), nullable=True),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), server_default='now()', nullable=False),
		sa.CheckConstraint('''
			( CASE WHEN host_id IS NULL THEN 0 ELSE 1 END
			+ CASE WHEN path_id IS NULL THEN 0 ELSE 1 END
			+ CASE WHEN machine_id IS NULL THEN 0 ELSE 1 END
			) > 0'''
		),
		sa.ForeignKeyConstraint(['host_id'], ['host.host_id'], ),
		sa.ForeignKeyConstraint(['machine_id'], ['machine.machine_id'], ),
		sa.ForeignKeyConstraint(['path_id'], ['path.path_id'], ),
		sa.ForeignKeyConstraint(['vulnerability_type_id'], ['vulnerability_type.vulnerability_type_id'], ),
		sa.PrimaryKeyConstraint('vulnerability_id')
	)
	op.execute("""
		CREATE TRIGGER host_audit
		AFTER INSERT OR UPDATE OR DELETE ON vulnerability
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")


def downgrade():
	op.drop_table('vulnerability')
	op.drop_index(op.f('ix_vulnerability_type_severity'), table_name='vulnerability_type')
	op.drop_index(op.f('ix_vulnerability_type_name'), table_name='vulnerability_type')
	
	op.drop_table('vulnerability_type')
	
	op.execute('drop type vulnerability_status_enum')