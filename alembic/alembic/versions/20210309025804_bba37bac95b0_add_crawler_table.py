"""add_crawler_table

Revision ID: bba37bac95b0
Revises: 444c7f1a4166
Create Date: 2021-03-09 02:58:04.265958

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bba37bac95b0'
down_revision = '444c7f1a4166'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('crawler',
		sa.Column('path_id', sa.Integer(), nullable=False),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), server_default=sa.text('to_timestamp(0)'), nullable=False),
		sa.ForeignKeyConstraint(['path_id'], ['path.path_id'], ),
		sa.PrimaryKeyConstraint('path_id'),
		schema='scans'
	)
	op.create_index(op.f('ix_scans_crawler_updated_dttm'), 'crawler', ['updated_dttm'], unique=False, schema='scans')
	op.execute("""
		CREATE TRIGGER host_audit
		AFTER INSERT OR UPDATE OR DELETE ON scans.crawler
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")



def downgrade():
	op.drop_table('crawler', schema='scans')

