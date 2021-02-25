import logging
import sqlalchemy
import sqlalchemy.orm
from configparser import ConfigParser


from commons.alchemyrepository import \
	HostRepository, \
	MachineRepository, \
	PathRepository

from src import Controller


def main():
	logger = logging.getLogger("AMASS")
	
	config = ConfigParser()
	config.read("commons/config.ini")

	engine = sqlalchemy.create_engine(
		'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(
			db_user=config["DB"]["user"],
			db_pass=config["DB"]["pass"],
			db_host=config["DB"]["host"],
			db_port=config["DB"]["port"],
			db_name=config["DB"]["name"]
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
