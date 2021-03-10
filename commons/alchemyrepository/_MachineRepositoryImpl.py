from sqlalchemy.orm import Session

from commons.domain.models import Machine
from commons.domain.repository import MachineRepository as definition

class MachineRepository(definition):
	def __init__(self,
				 session: Session):
		self.session = session

	def get_by_id(self,
				  machine_id: int) -> Machine:
		return self.session.query(Machine).filter(Machine.id == machine_id).first()

	def get_by_ip(self,
				  machine_ip: str) -> Machine:
		return self.session.query(Machine).filter(Machine.ip == machine_ip).first()

	def add(self,
			machine: Machine) -> Machine:
		self.session.add(machine)
		self.session.flush()
		return machine

	def safe_add(self,
				 machine: Machine) -> Machine:
		m = self.get_by_ip(machine.ip)
		if m is None:
			self.session.add(machine)
		else :
			machine = m
		self.session.flush()
		return machine

	def update(self,
			   machine: Machine) -> Machine:
		self.session.flush()
		return machine

	def delete(self,
			   machine: Machine):
		self.session.delete(machine)
