from abc import ABC, abstractmethod
from typing import Optional

from commons.domain.models import \
	Crawler, \
	Host, \
	Path

class CrawlerRepository(ABC):

	@abstractmethod
	def get_by_path(self,
					path: Path) -> Crawler:
		raise NotImplementedError()

	@abstractmethod
	def get_by_host(self,
					host: Host) -> Crawler:
		raise NotImplementedError()

	@abstractmethod
	def get_by_url(self,
				   url: str) -> Crawler:
		raise NotImplementedError()

	@abstractmethod
	def get_by_domain(self,
					  domain: str) -> Crawler:
		raise NotImplementedError()

	@abstractmethod
	def get_next(self, 
				 weeks: Optional[int] = 0,
				 days: Optional[int] = 0) -> Crawler:
		raise NotImplementedError()

	@abstractmethod
	def add_paths_to_crawler(self):
		raise NotImplementedError()

	@abstractmethod
	def add(self,
			crawler: Crawler) -> Crawler:
		raise NotImplementedError()

	@abstractmethod
	def update(self,
			   crawler: Crawler) -> Crawler:
		raise NotImplementedError()
