from abc import ABC, abstractmethod
from typing import List

from domain.models import Host

class HostRepository(ABC):

	@abstractmethod
	def get_by_id(self,
				  host_id: int) -> Host:
		raise NotImplementedError()

	@abstractmethod
	def get_by_domain(self,
					  domain: str) -> Host:
		raise NotImplementedError()

	@abstractmethod
	def add(self,
			host: Host) -> Host:
		raise NotImplementedError()

	@abstractmethod
	def update(self,
			   host: Host) -> Host:
		raise NotImplementedError()

