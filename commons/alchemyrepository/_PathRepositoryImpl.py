from sqlalchemy.orm import Session

from commons.domain.models import Path
from commons.domain.repository import PathRepository as definition

class PathRepository(definition):
	def __init__(self,
				 session: Session):
		self.session = session

	def get_by_id(self,
				  path_id: int) -> Path:
		return self.session.query(Path).filter(Path.id == path_id).first()

	def get_by_url(self,
				   url: str) -> Path:
		return self.session.query(Path).filter(Path.url == url).first()

	def add(self,
			path: Path) -> Path:
		self.session.add(path)
		self.session.flush()
		return path

	def update(self,
			   path: Path) -> Path:
		self.session.flush()
		return path
