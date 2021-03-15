import os
import logging
import sqlalchemy
import sqlalchemy.orm

from commons.alchemyrepository import \
	ConfigRepository, \
	HostRepository, \
	MachineRepository, \
	PathRepository

from commons.domain.models import Config

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

	config_repository = ConfigRepository(session)
	machine_repository = MachineRepository(session)
	host_repository = HostRepository(session)
	path_repository = PathRepository(session)

	config = config_repository.get_by_name("Amas")
	if config is None:
		logger.warning("Amas config not found, creating default")
		config = Config(
			name="Amas",
			config={
				"targets": []
			}
		)
		config = config_repository.add(config)
		session.commit()
		exit(2)

	targets = config.config["targets"]
	if targets == []:
		logger.critical("no target given")
		exit(1)


	controller = Controller(
		host_repository=host_repository,
		machine_repository=machine_repository,
		path_repository=path_repository,
		targets=targets,
		logger=logger
	)
	controller.execute()

	session.commit()

if __name__ == '__main__':
	main()
