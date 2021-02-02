import sqlalchemy
import sqlalchemy.orm
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

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
session = session_maker()

