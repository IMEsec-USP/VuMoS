from sqlalchemy.orm import Session
from datetime import datetime

from commons.domain.models import Config
from commons.domain.repository import ConfigRepository as definition

class ConfigRepository(definition):
	def __init__(self,
				 session: Session):
		self.session = session

	def get_by_id(self,
				  config_id: int) -> Config:
		return self.session.query(Config).filter(Config.id == config_id).first()

	def get_by_domain(self,
					  name: str) -> Config:
		return self.session.query(Config).filter(Config.name == name).first()

	def add(self,
			config: Config) -> Config:
		self.session.add(config)
		self.session.flush()
		return config
	
	def safe_add(self,
				 config: Config) -> Config:
		c = self.get_by_name(config.name)
		if c is None:
			self.session.add(config)
		else :
			c.config = config.config
			c.updated_dttm = datetime.now()
			self.session.expunge(config)
			config = c
		self.session.flush()
		return config

	def update(self,
			   config: Config) -> Config:
		self.session.flush()
		return config
