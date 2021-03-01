import os
import logging
import sqlalchemy
import sqlalchemy.orm


from commons.alchemyrepository import \
	HostRepository, \
	MachineRepository, \
	PathRepository

from src import Controller


def main():
	logger = logging.getLogger("AMASS")
	
	engine = sqlalchemy.create_engine(
		'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(
			db_user=os.environ.get("DB_USER"),
			db_pass=os.environ.get("DB_PASS"),
			db_name=os.environ.get("DB_NAME"),
			db_host=os.environ.get("DB_HOST"),
			db_port=os.environ.get("DB_PORT")
		)
	)

	session_maker = sqlalchemy.orm.sessionmaker(engine)
	session = session_maker(autoflush=False)

	machine_repository = MachineRepository(session)
	host_repository = HostRepository(session)
	path_repository = PathRepository(session)

	controller = Controller(
		host_repository=host_repository,
		machine_repository=machine_repository,
		path_repository=path_repository,
		logger=logger
	)
	controller.execute()

	session.commit()

if __name__ == '__main__':
	main()
