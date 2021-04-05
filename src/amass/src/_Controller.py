import json
import requests
import subprocess
import urllib3
from datetime import date
from logging import Logger
from difflib import SequenceMatcher
from retry import retry
from typing import List

from commons.domain.models import \
    Host, \
    Machine, \
    Path

from commons.domain.repository import \
    HostRepository, \
    MachineRepository, \
    PathRepository

class Controller(object):
    def __init__(self,
                 host_repository: HostRepository,
                 machine_repository: MachineRepository,
                 path_repository: PathRepository,
                 targets: List[str],
                 logger: Logger):
        self.host_repository = host_repository
        self.machine_repository = machine_repository
        self.path_repository = path_repository
        self.targets = targets
        self.logger = logger

    
    @retry(requests.exceptions.ConnectionError, tries=10, delay=1) 
    def make_wildcard_request(self, domain):
        return requests.get(f'http://asdfewcregonqwnsd.{domain}')

    def execute(self):
        for root in self.targets:

            self.logger.info(f"running amass to {root}")

            OUTPUT_PATH = f"outputs/{date.today()}.json"
            
            parameter = ["amass", "enum", "-src", "-noalts", "-d", root, "-json", OUTPUT_PATH, "-log", "logs/amass.log"]
            stdout = subprocess.run(parameter, stdout=subprocess.PIPE).stdout.decode("utf-8")

            self.logger.debug(f"-----------String de output do amass:-----------\n{stdout}\n------------------------------------------------")

            wildcard_cache = {}
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
                        
                        wildcard_request = wildcard_cache.get(domain, "Unknown")
                        if wildcard_request == "Unknown":
                            try:
                                wildcard_request = self.make_wildcard_request(domain)
                                wildcard_cache[domain] = wildcard_request

                            except urllib3.exceptions.MaxRetryError:
                                wildcard_request = None
                                wildcard_cache[domain] = wildcard_request

                            except requests.exceptions.ConnectionError: # Failed all retries defined in function
                                line = result.readline()
                                continue    

                        try:
                            r = requests.get(f"http://{subdomain}")
                            if r.status_code >= 500 or r.status_code < 400:
                                host = Host(
                                    domain=subdomain,
                                    machines=machines
                                )
                                if wildcard_request == None or wildcard_request.status_code != r.status_code or SequenceMatcher(None, wildcard_request.content, r.content).ratio() < 0.8:
                                    self.logger.debug(f"adding db_host to {subdomain}")
                                    host = self.host_repository.safe_add(host)
                                    path = Path(
                                            url=r.url,
                                            host=host,
                                            method='GET',
                                            vars={}
                                        )
                                    path = self.path_repository.safe_add(path)

                        except requests.exceptions.RequestException:
                            pass
                    else:
                        try:
                            r = requests.get(f"http://{subdomain}")
                            if r.status_code >= 500 or r.status_code < 400:
                                host = Host(
                                    domain=subdomain,
                                    machines=machines
                                )
                                self.logger.debug(f"adding root domain {subdomain} db")
                                host = self.host_repository.safe_add(host)
                                path = Path(
                                        url=r.url,
                                        host=host,
                                        method='GET',
                                        vars={}
                                        )
                                path = self.path_repository.safe_add(path)
                                
                        except requests.exceptions.RequestException:
                            pass

                    line = result.readline()
