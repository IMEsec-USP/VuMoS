import json
import requests
import subprocess
from logging import Logger
from difflib import SequenceMatcher

from commons.domain.models import \
	Host, \
	Machine

from commons.domain.repository import \
	HostRepository, \
	MachineRepository

class Controller(object):
	def __init__(self,
				 host_repository: HostRepository,
				 machine_repository: MachineRepository,
				 logger: Logger):
		self.host_repository = host_repository
		self.machine_repository = machine_repository
		self.logger = logger

	def execute(self):
		with open("scr/targets.json", 'r') as f:
			targets = json.loads(f.read())

		for root in targets:

			self.logger.info(f"running amass to {root}")

			OUTPUT_PATH = "output.json"
			parameter = ["amass", "enum", "-src", "-noalts", "-d", root, "-json", OUTPUT_PATH, "-log", "logs/amass.log"]
			stdout = subprocess.run(parameter, stdout=subprocess.PIPE).stdout.decode("utf-8")

			test_requests = {}
			machines_cache = {}

			with open(OUTPUT_PATH, "r") as result:

				line = result.readline()
				while line != '':

					line = json.loads(line)
					subdomain = line["name"]
					ips = [adress["ip"] for adress in line["addresses"]]

					machines = []
					for ip in ips:
						m = machines_cache.get(ip)
						if m is None:
							m = Machine(
								ip=ip
							)
							self.logger.debug(f"adding machine to ip {ip}")
							m = self.machine_repository.safe_add(m)
							machines_cache[ip] = m
						machines.append(m)

					if subdomain != root:
						domain = '.'.join(subdomain.split('.')[1:])
						
						base_request = test_requests.get(domain)
						if base_request is None:
							base_request = requests.get(f'http://asdfewcregonqwnsd.{domain}')
							test_requests[domain] = base_request

						try :
							r = requests.get(f"http://{subdomain}")
							if r.status_code >= 500 or r.status_code < 400:
								host = Host(
									domain=subdomain,
									machines=machines
								)
								if base_request.status_code != r.status_code or SequenceMatcher(None, base_request.content, r.content).ratio() < 0.8:
									self.logger.debug(f"adding db_host to {subdomain}")
									host = self.host_repository.safe_add(host)
						except requests.exceptions.RequestException:
							pass
					else:
						try :
							r = requests.get(f"http://{subdomain}")
							if r.status_code >= 500 or r.status_code < 400:
								host = Host(
									domain=subdomain,
									machines=machines
								)
								self.logger.debug(f"adding root domain {subdomain} db")
								host = self.host_repository.safe_add(host)
						except requests.exceptions.RequestException:
							pass

					line = result.readline()

