""" Abstract Class Modelling Basic Behaviors of any Item Represented in the DB
    These are a little bit nicer to work with than the tuples and dicts that the mysql Python API returns
"""


class DBItem:
	_db_state = 'no-init'
	_item_id = -1

	def is_valid(self):
		if self._db_state != '':
			return True

		return False

	def get_id(self):
		return self._item_id

	""" ABSTRACT: must be implemented by subclasses """
	def get_json(self):
		pass
