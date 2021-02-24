from abc import ABC, abstractmethod
from typing import List

from commons.domain.models import Host

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

	# save adding host will update machine_host relation, because it is easy for a host to look for the machines than the opposite
	@abstractmethod
	def safe_add(self,
				 host: Host) -> Host:
		raise NotImplementedError()

	@abstractmethod
	def update(self,
			   host: Host) -> Host:
		raise NotImplementedError()

