from datetime import datetime
from typing import Optional, List

from ._Host import Host

class Machine(object):
	def __init__(self,
				 id: int,
				 ip: int,
				 institute: str,
				 hosts: List[Host],
				 external: 	Optional[bool] = False,
				 updated_dttm: Optional[datetime] = datetime.now()
		):
		self.id = id
		self.ip = ip
		self.institute = institute
		self.hosts = hosts
		self.external = external
		self.updated_dttm = updated_dttm

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.__dict__)
