#!/usr/bin/env python3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from urllib.parse import urlparse

import os
import logging
import logging.config
import sqlalchemy
import sqlalchemy.orm
import yaml
from datetime import datetime

from commons.domain.models import \
	Host, \
	Machine, \
	Path

from commons.alchemyrepository import \
	CrawlerRepository, \
	ConfigRepository, \
	HostRepository, \
	MachineRepository, \
	PathRepository


class HDBSpider(CrawlSpider):
	name = "sqlsearch"
	allowed_domains = ["usp.br"]

	rules = (
		Rule(link_extractor=LxmlLinkExtractor(
			allow=(), unique=True), callback="parse", follow=False),
	)

	dynlink_extractor = LxmlLinkExtractor(
		allow=('\?'), canonicalize=True, unique=True, allow_domains="usp.br")

	def __init__(self):
		with open('/app/logging.yaml', 'r') as f:
			logging.config.dictConfig(yaml.load(f.read()))
		self.code_logger = logging.getLogger("Crawler")

		super(HDBSpider, self).__init__()
		alchemy_engine = sqlalchemy.create_engine(
			'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(
				db_user=os.environ.get("DB_USER"),
				db_pass=os.environ.get("DB_PASS"),
				db_name=os.environ.get("DB_NAME"),
				db_host=os.environ.get("DB_HOST"),
				db_port=os.environ.get("DB_PORT")
			)
		)

		session_maker = sqlalchemy.orm.sessionmaker(alchemy_engine)
		self.db_session = session_maker(autoflush=False)

		self.crawler_repository = CrawlerRepository(self.db_session)
		self.host_repository = HostRepository(self.db_session)
		self.path_repository = PathRepository(self.db_session)
		self.machine_repository = MachineRepository(self.db_session)
		self.config_repository = ConfigRepository(self.db_session)

	def start_requests(self):
		self.crawler_repository.add_paths_to_crawler()
		self.db_session.commit()
		while True:
			config = self.config_repository.get_by_name("Crawler").config
			redo_in = config["redo_in"]
			aux = self.crawler_repository.get_next(weeks=redo_in["weeks"], days=redo_in["days"])
			if aux is None:
				self.code_logger.info('staring crawler')
				break
			url = aux.path.url
			self.code_logger.debug(f"add to queue {url}")
			yield scrapy.Request(url, self.parse)
			aux.updated_dttm = datetime.now()
			self.crawler_repository.update(aux)
			self.db_session.commit()

	def parse(self, response):
		machine = Machine(ip=str(response.ip_address))
		machine = self.machine_repository.safe_add(machine)
		self.code_logger.debug(f"machine {machine.ip} found")

		actions = set()
		for form in response.css('form'):
			extracted_stuff = {
				'inputs': [
					{
						'name': input.xpath('@name').extract_first(),
						'type': input.xpath('@type').extract_first(),
						'value': input.xpath('@value').extract_first(),
						'placeholder': input.xpath('@placeholder').extract_first()
					} for input in form.css('input') if input.xpath('@name').extract_first()
				],
				'action': form.xpath('@action').extract_first(),
				'method': form.xpath('@method').extract_first(),

				}
			method = extracted_stuff["method"] if extracted_stuff["method"] else "get"

			if extracted_stuff["action"] and extracted_stuff["inputs"]:
				resolved_action = response.urljoin(extracted_stuff["action"])
				if method+resolved_action not in actions:
					actions.add(method+resolved_action)
					host = Host(
						domain=urlparse(resolved_action).netloc,
						machines=[machine]
					)
					host = self.host_repository.safe_add(host)
					path = Path(
						url=resolved_action,
						host=host,
						method=method,
						vars=extracted_stuff["inputs"]
					)
					path = self.path_repository.safe_add(path)
					self.code_logger.debug(f"found form {resolved_action}")

		dynlinks_cache = set()
		for link in self.dynlink_extractor.extract_links(response):
			link_base = link.url.split('?')[0]
			if link_base not in dynlinks_cache:
				dynlinks_cache.add(link_base)

				host = Host(
					domain=urlparse(link.url).netloc,
					machines=[machine]
				)
				host = self.host_repository.safe_add(host)
				link = link.url.split('?')[1:]
				var = []
				for l in link:
					entries = l.split("&")
					for entry in entries:
						v = entry.split("=")
						var.append({
							"name": v[0],
							"value": v[1]
						})

				path = Path(
					url=link_base,
					host=host,
					method='get',
					vars=var
				)
				path = self.path_repository.safe_add(path)
				self.code_logger.debug(f"found link {link_base}")

		self.db_session.commit()
