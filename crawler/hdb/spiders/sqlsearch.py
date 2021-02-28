#!/usr/bin/env python3

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from urllib.parse import urljoin, urlparse
from configparser import ConfigParser
import sqlalchemy
import sqlalchemy.orm
import sys
import os
sys.path.append(os.getcwd() + '/..')
from commons.domain.models import Host, Path
from commons.alchemyrepository import HostRepository, PathRepository

class HDBSpider(CrawlSpider):
    name = "sqlsearch"
    allowed_domains = ["usp.br"]
    start_urls = [
        'https://www5.usp.br/',
    ]

    rules = (
        Rule(link_extractor=LxmlLinkExtractor(allow=()), callback="parse", follow=True),
    )

    actions = set()
    base_dynlinks = set()

    dynlink_extractor = LxmlLinkExtractor(allow=('\?'), canonicalize=True, unique=True, allow_domains="usp.br")

    db_config = ConfigParser()
    db_config.read("../commons/config.ini")

    alchemy_engine = sqlalchemy.create_engine(
        'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(
            db_user=db_config["DB"]["user"],
            db_pass=db_config["DB"]["pass"],
            db_host=db_config["DB"]["host"],
            db_port=db_config["DB"]["port"],
            db_name=db_config["DB"]["name"]
        )
    )

    session_maker = sqlalchemy.orm.sessionmaker(alchemy_engine)
    db_session = session_maker(autoflush=False)

    host_repository = HostRepository(db_session)
    path_repository = PathRepository(db_session)


    def parse(self, response):
        out = {}
        out["url"] = response.url
        # out["forms"] = []
        out["sqlmap"] = []
        for form in response.css('form'):
            extracted_stuff = {
                'inputs': [
                    {
                        'name': input.xpath('@name').extract_first(),
                        'type': input.xpath('@type').extract_first(),
                        'value': input.xpath('@value').extract_first(),
                        'placeholder': input.xpath('@placeholder').extract_first(),
                    } for input in form.css('input') if input.xpath('@name').extract_first()
                ],
                'action': form.xpath('@action').extract_first(),
                'method': form.xpath('@method').extract_first(),

            }

            method = extracted_stuff["method"] if extracted_stuff["method"] else "get"
            if extracted_stuff["action"] and extracted_stuff["inputs"]:
                resolved_action = response.urljoin(extracted_stuff["action"])
                if method+resolved_action in self.actions:
                    continue
                else:
                    self.actions.add(method+resolved_action)
                host = Host(domain=urlparse(resolved_action).netloc)
                host = self.host_repository.safe_add(host)
                path = Path(
                    url=resolved_action,
                    host=host,
                    method=method,
                    vars=extracted_stuff["inputs"]
                )
                path = self.path_repository.safe_add(path)
                # out["forms"].append(extracted_stuff)
                sqlmap_querystr = ""
                if method.lower() == 'get':
                    sqlmap_querystr = f"-u '{resolved_action}?"
                else:
                    sqlmap_querystr = f"-u '{resolved_action}' --method={method} --data='"
                for input in extracted_stuff["inputs"]:
                    sqlmap_querystr += f"{input['name']}={input['value'] if input['value'] else 'a'}&"
                out["sqlmap"].append(sqlmap_querystr[:-1] +"\'")
        
        for link in self.dynlink_extractor.extract_links(response):
            linkoso_base = link.url.split('?')[0]
            if linkoso_base in self.base_dynlinks:
                continue
            else:
                self.base_dynlinks.add(linkoso_base)
                out["sqlmap"].append(f"-u '{link.url}'")
                host = Host(domain=urlparse(link.url).netloc)
                host = self.host_repository.safe_add(host)
                path = Path(
                    url=linkoso_base,
                    host=host,
                    method='get',
                    vars=link.url.split('?')[1:]
                )
                path = self.path_repository.safe_add(path)
        
        if out["sqlmap"]:
            self.db_session.commit()
            yield out
        
        # next_page = response.css('a::attr("href")').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
