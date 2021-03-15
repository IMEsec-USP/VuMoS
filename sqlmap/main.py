import os
import logging
import sqlalchemy
import sqlalchemy.orm
from time import sleep

from commons.alchemyrepository import \
	ConfigRepository, \
	MachineRepository, \
	NmapRepository

from commons.domain.models import Config

from src import Controller

def main():
	logging.basicConfig(
	    filename="logs/sqlmap.log",
		level=logging.INFO,
		format='%(asctime)s %(levelname)s:%(message)s'
	)
	logger = logging.getLogger("SQLMAP")
	logger.addHandler(logging.StreamHandler())
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

	config = config_repository.get_by_name("Sqlmap")
	if config is None:
		logger.error("Sqlmap config not found, creating default")
		config = Config(
			name="Sqlmap",
			config={
				"redo_in": {
					"weeks": 1,
					"days": 0
				},
				"outputfile": "nmap.xml"
			}
		)
		config = config_repository.add(config)

	controller = Controller(
		config= config.config,
		machine_repository=machine_repository,
		logger=logger
	)

	while True:
		wait = controller.execute()

		session.commit()

		if wait:
			sleep(60*60)

if __name__ == '__main__':
	main()