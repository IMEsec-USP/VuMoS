from abc import ABC, abstractmethod
from typing import List

from commons.domain.models import Machine

class MachineRepository(ABC):

	@abstractmethod
	def get_by_id(self,
				  machine_id: int) -> Machine:
		raise NotImplementedError()

	@abstractmethod
	def get_by_ip(self,
				  machine_ip: str) -> Machine:
		raise NotImplementedError()

	@abstractmethod
	def add(self,
			machine: Machine) -> Machine:
		raise NotImplementedError()

	# save adding machine NOT updates machine_host relation, because it is easy for a host to look for the machines than the opposite
	@abstractmethod
	def safe_add(self,
				 machine: Machine) -> Machine:
		raise NotImplementedError()

	@abstractmethod
	def update(self,
			   machine: Machine) -> Machine:
		raise NotImplementedError()

	@abstractmethod
	def delete(self,
			   machine: Machine):
		raise NotImplementedError()
