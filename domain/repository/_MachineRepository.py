from abc import ABC, abstractmethod
from typing import List

from domain.models import Machine

class MachineRepository(ABC):

	@abstractmethod
	def get_by_id(self,
				  chat_id: int) -> Machine:
		raise NotImplementedError()

	@abstractmethod
	def add(self,
			chat: Machine) -> Machine:
		raise NotImplementedError()
