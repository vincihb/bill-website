from db.model.ADBItem import ADBItem


class CongressionalSession(ADBItem):
	def __init__(self):
		pass

	def as_dict(self):
		return {
			'id': self._id
		}

	""" Database methods """
	def save(self):
		pass

	def get(self, _id):
		pass

	def _from_db(self, db_row):
		pass

	@staticmethod
	def from_db_object(db_object):
		cs = CongressionalSession()
		cs._from_db(db_object)
		return cs
