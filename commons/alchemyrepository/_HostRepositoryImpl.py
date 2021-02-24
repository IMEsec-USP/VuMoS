from sqlalchemy.orm import Session
from datetime import datetime

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
	
	def safe_add(self,
				 host: Host) -> Host:
		h = self.get_by_domain(host.domain)
		if h is None:
			self.session.add(host)
		else :
			h.machines = host.machines
			h.times_offline = 0
			h.access_dttm = datetime.now()
			self.session.expunge(host)
			host = h
		self.session.flush()
		return host

	def update(self,
			   host: Host) -> Host:
		self.session.flush()
		return host
