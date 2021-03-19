from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from commons.domain.models import Crawler, Host, Path
from commons.domain.repository import CrawlerRepository as definition

class CrawlerRepository(definition):
	def __init__(self,
				 session: Session):
		self.session = session

	def get_by_path(self,
					path: Path) -> Crawler:
		return self.session.query(Crawler).filter(Crawler.path == path).first()

	def get_by_host(self,
					host: Host) -> List[Crawler]:
		return self.session.query(Crawler).join(Path, Crawler.path_id == Path.id)\
			.filter(Path.host == host).all()

	def get_by_url(self,
				   url: str) -> Crawler:
		return self.session.query(Crawler).join(Path, Crawler.path_id == Path.id)\
			.filter(Path.url == url).first()

	def get_by_domain(self,
					  domain: str) -> List[Crawler]:
		return self.session.query(Crawler).join(Path, Crawler.path_id == Path.id)\
			.join(Host, Path.host_id == Path.id).filter(Host.domain == domain).all()

	def get_next(self, 
				 weeks: Optional[int] = 0,
				 days: Optional[int] = 0) -> Crawler:
		return self.session.query(Crawler)\
			.filter(Crawler.updated_dttm <= datetime.now() - timedelta(weeks=weeks, days=days))\
			.order_by(Crawler.updated_dttm).limit(1).first()

	def add_paths_to_crawler(self):
		self.session.execute("""
			INSERT into scans.crawler (path_id)
			select 
				p.path_id
			from 
				"path" p 
			left join scans.crawler c 
				ON p.path_id = c.path_id 
			where c.path_id is null
		""")

	def add(self,
			crawler: Crawler) -> Crawler:
		self.session.add(crawler)
		self.session.flush()
		return crawler

	def update(self,
			   crawler: Crawler) -> Crawler:
		self.session.flush()
		return crawler
