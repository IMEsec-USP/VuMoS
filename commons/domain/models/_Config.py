from datetime import datetime
from typing import Dict, Optional

class Config(object):
	def __init__(self,
				 name: str,
				 config: Optional[Dict] = {},
				 updated_dttm: Optional[datetime] = datetime.now()
		):
		self.id = None
		self.name = name
		self.config = config
		self.updated_dttm = updated_dttm

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.__dict__)
