from sqlalchemy import \
	Column, \
	ForeignKey, \
	Integer, \
	Table, \
	text

from sqlalchemy.orm import \
	mapper, \
	relationship

from sqlalchemy.dialects.postgresql import \
	JSON, \
	TIMESTAMP

from commons.domain.models import \
	Crawler, \
	Machine, \
	Nmap, \
	Path

class ScansMapper(object):
	def __init__(self, Base):
		self.Base = Base
		self.crawler = None
		self.nmap = None
		self.map()

	def map(self):
		self.crawler = Table(
			"crawler",
			self.Base,
			Column("path_id", Integer, ForeignKey("path.path_id"), nullable=False, primary_key=True),
			Column("updated_dttm", TIMESTAMP(), server_default=text('to_timestamp(0)'), nullable=False, index=True),
			schema="scans"
		)
		mapper(Crawler, self.crawler, properties={
			"path": relationship(Path, cascade="all, delete"),
			"updated_dttm": self.crawler.c.updated_dttm
		})

		self.nmap = Table(
			"nmap",
			self.Base,
			Column("machine_id", Integer, ForeignKey("machine.machine_id"), nullable=False, primary_key=True),
			Column("output", JSON),
			Column("updated_dttm", TIMESTAMP(), server_default=text('to_timestamp(0)'), nullable=False, index=True),
			schema="scans"
		)
		mapper(Nmap, self.nmap, properties={
			"machine": relationship(Machine, cascade="all, delete"),
			"output": self.nmap.c.output,
			"updated_dttm": self.nmap.c.updated_dttm
		})
