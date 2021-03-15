from datetime import datetime
from typing import Dict, Optional

from ._Path import Path

class Sqlmap(object):
	def __init__(self,
				 path: "Path",
				 clean: Optional[bool] = False,
				 output: Optional[Dict] = None,
				 updated_dttm: Optional[datetime] = None
		):
		self.path = path
		self.clean = clean
		self.output = output
		self.updated_dttm = updated_dttm

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.__dict__)
