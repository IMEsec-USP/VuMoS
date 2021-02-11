from sqlalchemy.orm import Session

from domain.models import Machine
from domain.repository import MachineRepository as definition

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

	def update(self,
			   machine: Machine) -> Machine:
		self.session.flush()
		return machine
