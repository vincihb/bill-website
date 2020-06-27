import json

""" 
	Abstract Class Modelling Basic Behaviors of any Item Represented in the DB
	These are a little bit nicer to work with than the tuples and dicts that the mysql Python API returns
"""


class ADBItem:
	_db_state = None
	_id = None

	def is_valid(self):
		if self._db_state is not None:
			return True

		return False

	def get_id(self):
		return self._id

	def get_api_data(self):
		return json.dumps(self.as_dict())

	""" ABSTRACT: must be implemented by subclasses """
	def save(self):
		raise ValueError('Method must be overridden')

	def get(self, _id):
		raise ValueError('Method must be overridden')

	def as_dict(self):
		raise ValueError('Method must be overridden')

	def _from_db(self, db_object):
		raise ValueError('Method must be overridden')

	@staticmethod
	def from_db(db_object):
		raise ValueError('Method must be overridden')
