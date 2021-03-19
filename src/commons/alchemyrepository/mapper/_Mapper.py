from sqlalchemy import MetaData

from ._PublicMapper import PublicMapper
from ._ScansMapper import ScansMapper

Base = MetaData()

class Mapper(object):
	def __init__(self):
		PublicMapper(Base)
		ScansMapper(Base)

Mapper()