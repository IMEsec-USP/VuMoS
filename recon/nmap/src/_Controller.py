import subprocess
from typing import Dict
from logging import Logger
from datetime import datetime
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

from commons.domain.repository import \
	MachineRepository, \
	NmapRepository

class Controller(object):
	def __init__(self,
				 config: Dict,
				 machine_repository: MachineRepository,
				 nmap_repository: NmapRepository,
				 logger: Logger):
		self.config = config
		self.machine_repository = machine_repository
		self.nmap_repository = nmap_repository
		self.logger = logger

	def run(self):
		self.logger.debug(f"config = {self.config}")
		outputfile = self.config["outputfile"]
		
		self.nmap_repository.add_machines_to_nmap()

		redo_in = self.config["redo_in"]

		nmap = self.nmap_repository.get_next(weeks=redo_in["weeks"], days=redo_in["days"])

		if nmap is None:
			return 1

		self.logger.info(f"starting nmap to {nmap.machine.ip}")

		parameter = self.config["run"].format(outputfile=outputfile, target=nmap.machine.ip).split()
		subprocess.run(parameter).stdout

		with open(outputfile, 'r') as f:
			output = bf.data(fromstring(f.read()))

		self.logger.info("saving")

		nmap.output = output
		nmap.updated_dttm = datetime.now()

		nmap = self.nmap_repository.update(nmap)

		return 0
