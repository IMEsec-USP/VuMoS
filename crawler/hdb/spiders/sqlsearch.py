#!/usr/bin/env python3

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from urllib.parse import urljoin, urlparse
import sqlalchemy
import sqlalchemy.orm
import sys
import os

from commons.domain.models import \
	Config, \
	Host, \
	Path

from commons.alchemyrepository import \
	ConfigRepository, \
	HostRepository, \
	PathRepository

class HDBSpider(CrawlSpider):
	name = "sqlsearch"
	allowed_domains = ["usp.br"]
	start_urls = [
		'http://www.reitoria.usp.br/',
	]

	rules = (
		Rule(link_extractor=LxmlLinkExtractor(allow=(), unique=True), callback="parse", follow=False),
	)

	dynlink_extractor = LxmlLinkExtractor(allow=('\?'), canonicalize=True, unique=True, allow_domains="usp.br")

	def __init__(self):
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

		self.host_repository = HostRepository(self.db_session)
		self.path_repository = PathRepository(self.db_session)
		config_repository = ConfigRepository(self.db_session)


	def parse(self, response):
		out = {}
		out["url"] = response.url
		out["sqlmap"] = []
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
				
				host = Host(domain=urlparse(resolved_action).netloc)
				host = self.host_repository.safe_add(host)
				path = Path(
					url=resolved_action,
					host=host,
					method=method,
					vars=extracted_stuff["inputs"]
				)
				path = self.path_repository.safe_add(path)

		
		for link in self.dynlink_extractor.extract_links(response):
			link_base = link.url.split('?')[0]
		
			host = Host(domain=urlparse(link.url).netloc)
			host = self.host_repository.safe_add(host)
			path = Path(
				url=link_base,
				host=host,
				method='get',
				vars=link.url.split('?')[1:]
			)
			path = self.path_repository.safe_add(path)
		
		self.db_session.commit()

