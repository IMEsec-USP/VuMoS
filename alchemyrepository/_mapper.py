from sqlalchemy import \
	Boolean, \
	Column, \
	ForeignKey, \
	Integer, \
	MetaData, \
	String, \
	Table, \
	TEXT

from sqlalchemy.orm import \
	mapper, \
	relationship

from sqlalchemy.dialects.postgresql import \
	INET, \
	SMALLINT, \
	TIMESTAMP

from domain.models import \
	Host, \
	Link, \
	Machine

Base = MetaData()

class Mapper(object):
	def __init__(self):
		self.machine = None
		self.host = None
		self.machine_domain = None
		self.link = None
		self.map()

	def map(self):
		self.machine = Table(
			"machine",
			Base,
			Column("machine_id", Integer, primary_key=True),
			Column("ip", INET, unique=True, nullable=False, index=True),
			Column("institute", TEXT),
			Column("external", Boolean, nullable=False, server_defalt='false'),
			Column("updated_dttm", TIMESTAMP, server_defalt='now()', nullable=False),
			# schema=""
		)
		mapper(Machine, self.machine, properties={
			"id": self.machine.c.machine_id,
			"ip": self.machine.c.ip,
			"hosts": relationship(Host, secondary=association_table, back_populates="machines"),
			"external": self.machine.c.external,
			"institute": self.machine.c.institute,
			"updated_dttm": self.machine.c.updated_dttm
		})

		self.host = Table(
			"host",
			Base,
			Column("host_id", Integer, primary_key=True),
			Column("domain", String(128), unique=True, nullable=False, index=True),
			Column("added_dttm", TIMESTAMP, server_defalt='now()', nullable=False),
			Column("access_dttm", TIMESTAMP, server_defalt='now()', nullable=False),
			Column("times_offline", SMALLINT, server_defalt='0', nullable=False),
			Column("updated_dttm", TIMESTAMP, server_defalt='now()', nullable=False),
			# schema=""
		)
		mapper(Host, self.host, properties={
			"id": self.host.c.host_id,
			"domain": self.host.c.domain,
			"machines": relationship(Machine, secondary=association_table, back_populates="hosts")
			"access_dttm": self.host.c.access_dttm,
			"times_offline": self.host.c.times_offline,
			"updated_dttm": self.host.c.updated_dttm
		})

		self.machine_host = Table(
			"machine_host",
			Base,
			Column("host_id", Integer, ForeignKey(self.host.c.host_id), nullable=False, primary_key=True),
			Column("machine_id", Integer, ForeignKey(self.machine.c.machine_id), nullable=False, primary_key=True),
			Column("updated_dttm", TIMESTAMP, server_defalt='now()', nullable=False),
			# schema=""
		)
		
		self.link = Table(
			"link",
			Base,
			Column("link_id", Integer, primary_key=True),
			Column("host_id", Integer, ForeignKey(self.host.c.host_id), nullable=False),
			Column("url", String(128), unique=True, nullable=False, index=True),
			Column("added_dttm", TIMESTAMP, server_defalt='now()', nullable=False),
			Column("access_dttm", TIMESTAMP, server_defalt='now()', nullable=False),
			Column("times_offline", SMALLINT, server_defalt='0', nullable=False),
			Column("updated_dttm", TIMESTAMP, server_defalt='now()', nullable=False),
			# schema=""
		)
		mapper(Link, self.link, properties={
			"id": self.link.c.link_id,
			"url": self.link.c.url,
			"host": relationship(Host, remote_side=[self.link.c.host_id])
			"access_dttm": self.link.c.access_dttm,
			"times_offline": self.link.c.times_offline,
			"updated_dttm": self.link.c.updated_dttm
		})

Mapper()