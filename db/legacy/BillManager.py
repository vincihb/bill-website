from db.legacy.Bill import Bill

"""
	Class built for interaction with the rest of the world, the raw Bill class can be used
	but the BillSqlProxy should NOT
"""


class BillManager:
	# BillSqlProxy()
	_proxy = None

	def parse_request(self, data: dict):
		if 'bill_id' in data:
			return self.get_single(bill_id=int(data['bill_id']))

		return ''

	def get_single(self, bill_id=-1):
		return self._unbox(self._proxy.get_by_id(bill_id))

	def get_multiple(self):
		pass

	def create_new_bill(self, name='', author='', state=''):
		new_bill = Bill(title=name, state=state, author=author)
		self._proxy.insert(new_bill)

	def _unbox_to_multiple(self, query_result):
		for item in query_result:
			self._unbox(item)

	def _unbox(self, query_result: tuple):
		if query_result == tuple() or query_result == (0,) or len(query_result) == 0:
			return ''

		if len(query_result) > 1:
			return self._unbox_to_multiple(query_result)
		else:
			res = query_result[0]
			return Bill(bill_id=res['id'], title=res['name'], author=res['author'], state=res['state'], bill_exists=True)

	@staticmethod
	def get_bill_from_propublica_data(bill: dict):
		return Bill(title=bill['name'], )

	def insert_bill(self, bill: Bill):
		pass
