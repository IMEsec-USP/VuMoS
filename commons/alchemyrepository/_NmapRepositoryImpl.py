from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from commons.domain.models import Nmap, Machine
from commons.domain.repository import NmapRepository as definition

class NmapRepository(definition):
	def __init__(self,
				 session: Session):
		self.session = session

	def get_by_machine(self,
					   machine: Machine) -> Nmap:
		return self.session.query(Nmap).filter(Nmap.machine == machine).first()

	def get_by_ip(self,
				  machine_ip: str) -> Nmap:
		return self.session.query(Nmap).join(Machine, Nmap.machine_id == Machine.id)\
			.filter(Machine.ip == machine_ip).first()

	def get_next(self, 
				 weeks: Optional[int] = 0,
				 days: Optional[int] = 0) -> Nmap:
		return self.session.query(Nmap)\
			.filter(Nmap.updated_dttm <= datetime.now() - timedelta(weeks=weeks, days=days))\
			.order_by(Nmap.updated_dttm).limit(1).first()

	def add_machines_to_nmap(self):
		self.session.execute("""
			INSERT into scans.nmap (machine_id)
			select 
				m.machine_id
			from 
				machine m 
			left join scans.nmap n 
				ON m.machine_id = n.machine_id 
			where n.machine_id is null
		""")

	def add(self,
			nmap: Nmap) -> Nmap:
		self.session.add(nmap)
		self.session.flush()
		return nmap

	def update(self,
			   nmap: Nmap) -> Nmap:
		self.session.flush()
		return nmap
