from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from commons.domain.models import Sqlmap, Host, Path
from commons.domain.repository import SqlmapRepository as definition

class SqlmapRepository(definition):
	def __init__(self,
				 session: Session):
		self.session = session

	def get_by_path(self,
					path: Path) -> Sqlmap:
		return self.session.query(Sqlmap).filter(Sqlmap.path == path).first()

	def get_by_host(self,
					host: Host) -> List[Sqlmap]:
		return self.session.query(Sqlmap).join(Path, Sqlmap.path_id == Path.id)\
			.filter(Path.host == host).all()

	def get_by_url(self,
				   url: str) -> Sqlmap:
		return self.session.query(Sqlmap).join(Path, Sqlmap.path_id == Path.id)\
			.filter(Path.url == url).first()

	def get_by_domain(self,
					  domain: str) -> List[Sqlmap]:
		return self.session.query(Sqlmap).join(Path, Sqlmap.path_id == Path.id)\
			.join(Host, Path.host_id == Path.id).filter(Host.domain == domain).all()

	def get_next(self, 
				 weeks: Optional[int] = 0,
				 days: Optional[int] = 0) -> Sqlmap:
		return self.session.query(Sqlmap)\
			.filter(Sqlmap.clean == False)\
			.filter(Sqlmap.updated_dttm <= datetime.now() - timedelta(weeks=weeks, days=days))\
			.order_by(Sqlmap.updated_dttm).limit(1).first()

	def add_paths_to_sqlmap(self):
		self.session.execute("""
			INSERT into scans.sqlmap (path_id)
			select 
				p.path_id
			from 
				"path" p 
			left join scans.sqlmap c 
				ON p.path_id = c.path_id 
			where c.path_id is null
		""")

	def add(self,
			sqlmap: Sqlmap) -> Sqlmap:
		self.session.add(sqlmap)
		self.session.flush()
		return sqlmap

	def update(self,
			   sqlmap: Sqlmap) -> Sqlmap:
		self.session.flush()
		return sqlmap
