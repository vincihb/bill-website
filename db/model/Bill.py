from db.model.ADBItem import ADBItem

"""
Class for interface with specific bills
"""


class Bill(ADBItem):
	_active = True
	AUTHOR = ''
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
	STATE = ''  # the easily human-readable version
	TITLE = ''  # refers to the short_title
	_vetoed = False
	BILL_ID = None

	def __init__(self):
		pass

	def save(self):
		pass

	def get(self, _id):
		pass

	""" Helper Methods """
	def as_dict(self):
		return {
			'bill_id': self._id,
			'state': self.STATE,
			'author': self.AUTHOR,
			'name': self.TITLE
		}

	def _from_db(self, db_object):
		self.TITLE = db_object.get('TITLE')
		self.AUTHOR = db_object.get('AUTHOR')
		self.BILL_ID = db_object.get('BILL_ID')
		self._id = db_object.get('id')

	@staticmethod
	def from_db(db_object):
		bill = Bill()
		bill._from_db(db_object)
		return bill
