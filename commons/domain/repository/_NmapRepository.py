from abc import ABC, abstractmethod
from typing import List

from commons.domain.models import \
	Machine, \
	Nmap

class NmapRepository(ABC):

	@abstractmethod
	def get_by_machine(self,
					   machine: Machine) -> Nmap:
		raise NotImplementedError()

	@abstractmethod
	def get_by_ip(self,
				  machine_ip: str) -> Nmap:
		raise NotImplementedError()

	@abstractmethod
	def get_next(self) -> Nmap:
		raise NotImplementedError()

	@abstractmethod
	def add_machines_to_nmap(self):
		raise NotImplementedError()

	@abstractmethod
	def add(self,
			nmap: Nmap) -> Nmap:
		raise NotImplementedError()

	@abstractmethod
	def update(self,
			   nmap: Nmap) -> Nmap:
		raise NotImplementedError()
