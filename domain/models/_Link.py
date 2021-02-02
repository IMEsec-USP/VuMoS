from datetime import datetime
from typing import Optional

from ._Host import Host

class Link(object):
	def __init__(self,
				 id: int,
				 url: str,
				 host: Host,
				 times_offline: Optional[int] = 0,
				 access_dttm: Optional[datetime] = datetime.now(),
				 updated_dttm: Optional[datetime] = datetime.now()
		):
		self.id = id
		self.url = url
		self.host = host
		self.access_dttm = access_dttm
		self.updated_dttm = updated_dttm
		self.times_offline = times_offline

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.__dict__)
