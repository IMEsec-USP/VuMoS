from sqlalchemy.orm import Session

from commons.domain.models import Host
from commons.domain.repository import HostRepository as definition

class HostRepository(definition):
	def __init__(self,
				 session: Session):
		self.session = session

	def get_by_id(self,
				  host_id: int) -> Host:
		return self.session.query(Host).filter(Host.id == host_id).first()

	def get_by_domain(self,
					  domain: str) -> Host:
		return self.session.query(Host).filter(Host.domain == domain).first()

	def add(self,
			host: Host) -> Host:
		self.session.add(host)
		self.session.flush()
		return host
	
	def update(self,
			   host: Host) -> Host:
		self.session.flush()
		return host
