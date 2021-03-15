from abc import ABC, abstractmethod
from typing import Optional, List

from commons.domain.models import \
	Host, \
	Path, \
	Sqlmap

class SqlmapRepository(ABC):

	@abstractmethod
	def get_by_path(self,
					path: Path) -> Sqlmap:
		raise NotImplementedError()

	@abstractmethod
	def get_by_host(self,
					host: Host) -> List[Sqlmap]:
		raise NotImplementedError()

	@abstractmethod
	def get_by_url(self,
				   url: str) -> Sqlmap:
		raise NotImplementedError()

	@abstractmethod
	def get_by_domain(self,
					  domain: str) -> List[Sqlmap]:
		raise NotImplementedError()

	@abstractmethod
	def get_next(self, 
				 weeks: Optional[int] = 0,
				 days: Optional[int] = 0) -> Sqlmap:
		raise NotImplementedError()

	@abstractmethod
	def add_paths_to_sqlmap(self):
		raise NotImplementedError()

	@abstractmethod
	def add(self,
			sqlmap: Sqlmap) -> Sqlmap:
		raise NotImplementedError()

	@abstractmethod
	def update(self,
			   sqlmap: Sqlmap) -> Sqlmap:
		raise NotImplementedError()
