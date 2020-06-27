import json
from db.DBItem import DBItem


class CongressCache(DBItem):
	_photo_url = ''
	_first_name = ''
	_last_name = ''
	_full_name = ''
	_credit = ''
	_cache_date = ''

	def __init__(
			self, cache_exists=False, first_name='', last_name='', full_name='', photo_url='', credit='', cache_id=-1
	):
		if cache_exists:
			self._item_id = cache_id
			self._db_state = 'in-db'

		self._first_name = first_name
		self._last_name = last_name
		self._full_name = full_name
		self._photo_url = photo_url
		self._credit = credit

	""" Getters """
	def get_first_name(self):
		return self._first_name

	def get_last_name(self):
		return self._first_name

	def get_name(self):
		return self._full_name

	def get_url(self):
		return self._photo_url

	""" Setters """
	def set_first_name(self, name):
		self._first_name = name

	def set_last_name(self, name):
		self._last_name = name

	def set_full_name(self, name):
		self._full_name = name

	def set_photo_url(self, url):
		self._photo_url = url

	""" implement abstract methods """
	def get_json(self):
		return json.dumps(
			{
				'first': self._first_name, 'last': self._last_name, 'fullName': self._full_name, 'id': self._item_id,
				'photoUrl': self._photo_url, 'credit': self._credit
			}
		)

	""" Database methods """
	def insert(self):
		pass

	def update(self):
		pass

	def get(self):
		pass

	def delete(self):
		pass

	""" Other Helpers """
	def available(self):
		return True if self._photo_url != '' else False
