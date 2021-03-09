from datetime import datetime
from typing import Optional

from ._Path import Path

class Crawler(object):
	def __init__(self,
				 path: "Path",
				 updated_dttm: Optional[datetime] = None
		):
		self.path = path
		self.updated_dttm = updated_dttm

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.__dict__)
