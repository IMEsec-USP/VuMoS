import os
import logging
import logging.config
import sqlalchemy
import sqlalchemy.orm
import subprocess
import yaml
from time import sleep

from commons.alchemyrepository import \
	CrawlerRepository, \
	ConfigRepository

from commons.domain.models import Config

def main():
	with open('/app/logging.yaml', 'r') as f:
			logging.config.dictConfig(yaml.load(f.read(), Loader=yaml.FullLoader))
	logger = logging.getLogger("Crawler")

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
	crawler_repository = CrawlerRepository(session)

	config = config_repository.get_by_name("Crawler")
	if config is None:
		config = Config(
			name="Crawler",
			config={
				"redo_in": {
					"weeks": 1,
					"days": 0
				},
				"sleep": {
					"seconds": 0,
					"minutes": 0,
					"hours": 1
				}
			}
		)
		config = config_repository.add(config)


	while True:
		redo_in = config_repository.get_by_name("Crawler").config['redo_in']
		crawler_repository.add_paths_to_crawler()
		aux = crawler_repository.get_next(weeks=redo_in["weeks"], days=redo_in["days"])
		if aux is None:
			logger.warning(f"no target to scan")
			seconds = config.config["sleep"]["seconds"] + 60*config.config["sleep"]["minutes"] + 3600*config.config["sleep"]["hours"]
			sleep(seconds)
		else:
			subprocess.run("python -m scrapy crawl sqlsearch -o /dev/stdout:json".split()).stdout

if __name__ == '__main__':
	main()
