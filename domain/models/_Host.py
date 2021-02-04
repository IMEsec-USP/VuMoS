from datetime import datetime
from typing import List, Optional

class Host(object):
	def __init__(self,
				 domain: str,
				 machines: Optional[List["Machine"]] = [],
				 times_offline: Optional[int] = 0,
				 access_dttm: Optional[datetime] = datetime.now(),
				 updated_dttm: Optional[datetime] = datetime.now()
		):
		self.id = None
		self.domain = domain
		self.machines = machines
		self.times_offline = times_offline
		self.added_dttm = None
		self.access_dttm = access_dttm
		self.updated_dttm = updated_dttm

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.__dict__)
