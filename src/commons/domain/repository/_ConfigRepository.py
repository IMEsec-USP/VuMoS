from abc import ABC, abstractmethod
from typing import List

from commons.domain.models import Config

class ConfigRepository(ABC):

	@abstractmethod
	def get_by_id(self,
				  config_id: int) -> Config:
		raise NotImplementedError()

	@abstractmethod
	def get_by_name(self,
					  name: str) -> Config:
		raise NotImplementedError()

	@abstractmethod
	def add(self,
			host: Config) -> Config:
		raise NotImplementedError()

	@abstractmethod
	def safe_add(self,
				 host: Config) -> Config:
		raise NotImplementedError()

	@abstractmethod
	def update(self,
			   host: Config) -> Config:
		raise NotImplementedError()

