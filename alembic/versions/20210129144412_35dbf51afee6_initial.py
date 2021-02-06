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
	op.execute("""
		CREATE schema if not exists audit;
		revoke create on schema audit from public;

		create table if not exists audit.logged_actions (
			schema_name text not null,
			table_name text not null,
			user_name text,
			action_tstamp timestamp with time zone not null default current_timestamp,
			action TEXT NOT NULL check (action in ('I','D','U')),
			original_data text,
			new_data text,
			query text
		) with (fillfactor=100);

		revoke all on audit.logged_actions from public;

		-- You may wish to use different permissions; this lets anybody
		-- see the full audit data. In Pg 9.0 and above you can use column
		-- permissions for fine-grained control.
		grant select on audit.logged_actions to public;

		create index logged_actions_schema_table_idx 
		on audit.logged_actions(((schema_name||'.'||table_name)::TEXT));

		create index logged_actions_action_tstamp_idx 
		on audit.logged_actions(action_tstamp);

		create index logged_actions_action_idx 
		on audit.logged_actions(action);
	""")

	op.execute("""
		CREATE OR REPLACE FUNCTION audit.if_modified_func() RETURNS trigger AS $body$
		DECLARE
			v_old_data TEXT;
			v_new_data TEXT;
		BEGIN
			/*  If this actually for real auditing (where you need to log EVERY action),
				then you would need to use something like dblink or plperl that could log outside the transaction,
				regardless of whether the transaction committed or rolled back.
			*/
			if (TG_OP = 'UPDATE') then
				v_old_data := ROW(OLD.*);
				v_new_data := ROW(NEW.*);
				insert into audit.logged_actions (schema_name,table_name,user_name,action,original_data,new_data,query) 
				values (TG_TABLE_SCHEMA::TEXT,TG_TABLE_NAME::TEXT,session_user::TEXT,substring(TG_OP,1,1),v_old_data,v_new_data, current_query());
				RETURN NEW;
			elsif (TG_OP = 'DELETE') then
				v_old_data := ROW(OLD.*);
				insert into audit.logged_actions (schema_name,table_name,user_name,action,original_data,query)
				values (TG_TABLE_SCHEMA::TEXT,TG_TABLE_NAME::TEXT,session_user::TEXT,substring(TG_OP,1,1),v_old_data, current_query());
				RETURN OLD;
			elsif (TG_OP = 'INSERT') then
				v_new_data := ROW(NEW.*);
				insert into audit.logged_actions (schema_name,table_name,user_name,action,new_data,query)
				values (TG_TABLE_SCHEMA::TEXT,TG_TABLE_NAME::TEXT,session_user::TEXT,substring(TG_OP,1,1),v_new_data, current_query());
				RETURN NEW;
			else
				RAISE WARNING '[AUDIT.IF_MODIFIED_FUNC] - Other action occurred: %, at %',TG_OP,now();
				RETURN NULL;
			end if;

		EXCEPTION
			WHEN data_exception THEN
				RAISE WARNING '[AUDIT.IF_MODIFIED_FUNC] - UDF ERROR [DATA EXCEPTION] - SQLSTATE: %, SQLERRM: %',SQLSTATE,SQLERRM;
				RETURN NULL;
			WHEN unique_violation THEN
				RAISE WARNING '[AUDIT.IF_MODIFIED_FUNC] - UDF ERROR [UNIQUE] - SQLSTATE: %, SQLERRM: %',SQLSTATE,SQLERRM;
				RETURN NULL;
			WHEN others THEN
				RAISE WARNING '[AUDIT.IF_MODIFIED_FUNC] - UDF ERROR [OTHER] - SQLSTATE: %, SQLERRM: %',SQLSTATE,SQLERRM;
				RETURN NULL;
		END;
		$body$
		LANGUAGE plpgsql
		SECURITY DEFINER
		SET search_path = pg_catalog, audit;
	""")


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
	op.execute("""
		CREATE TRIGGER host_audit
		AFTER INSERT OR UPDATE OR DELETE ON host
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")

	op.create_table('machine',
		sa.Column('machine_id', sa.Integer(), nullable=False),
		sa.Column('ip', postgresql.INET(), nullable=False),
		sa.Column('institute', sa.TEXT(), nullable=True),
		sa.Column('external', sa.Boolean(), nullable=False, server_default='false'),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.PrimaryKeyConstraint('machine_id')
	)
	op.create_index(op.f('ix_machine_ip'), 'machine', ['ip'], unique=True)
	op.execute("""
		CREATE TRIGGER machine_audit
		AFTER INSERT OR UPDATE OR DELETE ON machine
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")

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
	op.execute("""
		CREATE TRIGGER path_audit
		AFTER INSERT OR UPDATE OR DELETE ON "path"
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")

	op.create_table('machine_host',
		sa.Column('host_id', sa.Integer(), nullable=False),
		sa.Column('machine_id', sa.Integer(), nullable=False),
		sa.Column('updated_dttm', postgresql.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
		sa.ForeignKeyConstraint(['host_id'], ['host.host_id'], ),
		sa.ForeignKeyConstraint(['machine_id'], ['machine.machine_id'], ),
		sa.PrimaryKeyConstraint('host_id', 'machine_id')
	)
	op.execute("""
		CREATE TRIGGER machine_host_audit
		AFTER INSERT OR UPDATE OR DELETE ON machine_host
		FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func();
	""")


def downgrade():
	op.drop_table('machine_host')
	op.drop_index(op.f('ix_path_url'), table_name='path')
	op.drop_table('path')
	op.drop_index(op.f('ix_machine_ip'), table_name='machine')
	op.drop_table('machine')
	op.drop_index(op.f('ix_host_domain'), table_name='host')
	op.drop_table('host')
