from abc import ABC, abstractmethod
from typing import List

from commons.domain.models import Path

class PathRepository(ABC):

	@abstractmethod
	def get_by_id(self,
				  path_id: int) -> Path:
		raise NotImplementedError()

	@abstractmethod
	def get_by_url(self,
				   url: str) -> Path:
		raise NotImplementedError()

	@abstractmethod
	def add(self,
			path: Path) -> Path:
		raise NotImplementedError()

	@abstractmethod
	def update(self,
			   path: Path) -> Path:
		raise NotImplementedError()
