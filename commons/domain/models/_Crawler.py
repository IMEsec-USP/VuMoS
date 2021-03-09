from datetime import datetime
from typing import Dict, Optional

class Crawler(object):
	def __init__(self,
				 path: "Path",
				 updated_dttm: Optional[datetime] = None
		):
		self.machine = machine
		self.updated_dttm = updated_dttm

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.__dict__)
