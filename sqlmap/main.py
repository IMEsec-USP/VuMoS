import os
import logging
import sqlalchemy

from commons.alchemyrepository import \
	ConfigRepository, \
	VulnerabilityRepository, \
	SqlmapRepository

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
	vulnerability_repository = VulnerabilityRepository(session)
	sqlmap_repository = SqlmapRepository(session)

	controller = Controller(
		config_repository= config_repository,
		vulnerability_repository=vulnerability_repository,
		sqlmap_repository=sqlmap_repository,
		logger=logger
	)

	config = config_repository.get_by_name("Sqlmap")
	if config is None:
		logger.error("Sqlmap config not found, creating default")
		config = Config(
			name="Sqlmap",
			config={
				"sleep": {
					"seconds": 0,
					"minutes": 0,
					"hours": 1
				},
				"redo_in": {
					"weeks": 1,
					"days": 0
				},
				"outputfile": "nmap.xml"
			}
		)
		config = config_repository.add(config)
		session.commit()

	while True:
		status = controller.run()
		if status == 0:
			session.commit()
		else:
			break

if __name__ == '__main__':
	main()
