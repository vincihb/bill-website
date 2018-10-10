from DatabaseManager import dbm
from HMException import HMException


class SQLProxy:

	""" Queries Without DB Impact """
	@staticmethod
	def get_by_id(item_id):
		if item_id > -1:
			query = 'SELECT * FROM bill WHERE id=' + str(item_id)
			return dbm.reception_query(query_string=query)
		else:
			raise HMException('Invalid index argument to Bill.query_by_id')

	def insert(self):
		pass

	def update(self):
		pass

	def delete(self):
		pass

	def select(self):
		pass

	def get(self):
		pass
