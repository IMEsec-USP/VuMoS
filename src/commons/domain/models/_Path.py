from datetime import datetime
from typing import Optional, Dict

from ._Host import Host 

class Path(object):
	def __init__(self,
				 url: str,
				 host: Host,
				 method: str,
				 vars: Dict,
				 times_offline: Optional[int] = 0,
				 access_dttm: Optional[datetime] = datetime.now(),
				 updated_dttm: Optional[datetime] = datetime.now()
		):
		self.id = None
		self.url = url
		self.host = host
		self.method = method
		self.vars = vars
		self.access_dttm = access_dttm
		self.updated_dttm = updated_dttm
		self.times_offline = times_offline

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.__dict__)
