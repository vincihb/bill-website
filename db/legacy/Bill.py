import json
from db.legacy.DBItem import DBItem

"""
Class for interface with specific bills
"""


class Bill(DBItem):
	_active = True
	_author = ''
	_bill_url = ''  # propublica.org url -- bill_uri
	_committees = list()  # hold on to all associated committees in a list (using their committee codes)
	_congress_url = ''  # congress.gov url
	_long_summary = ''  # the actual summary (can be null)
	_history = dict()   # dict of dicts for easy json conversion, {introduced: {date: <date>, success: <boolean>},
						#											house: {...}, congress: {...}, president {...},
						# 											law: {date: <date>, }}
	_number = ''
	_slug = ''
	_short_summary = ''  # refers to the title
	_sponsor_party = ''  # R, D or I
	_state = ''  # the easily human-readable version
	_title = ''  # refers to the short_title
	_vetoed = False

	def __init__(self, bill_exists=False, title='', author='', state='invalid', bill_id=-1):
		if bill_exists:
			self._db_state = 'in-db'

		self._item_id = bill_id
		self.set_title(title)
		self.set_author(author)
		self.set_state(state)

	""" Setters """
	def set_title(self, name):
		self._title = name

	def set_state(self, state):
		self._update_history(self._state)
		self._state = state

	def set_author(self, author):
		self._author = author

	def _update_history(self, addition):
		if 'addition' in self._history.keys():
			self._history['addition'] += addition

	""" Getters """
	def get_title(self):
		return self._title

	def get_state(self):
		return self._state

	def get_author(self):
		return self._author

	def get_db_status(self):
		return self._db_state

	def get_history(self):
		return self._history

	""" Helper Methods """
	def get_json(self):
		return json.dumps(
			{'bill_id': self._item_id, 'state': self._state, 'author': self._author, 'name': self._title}
		)
