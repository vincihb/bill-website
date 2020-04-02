import requests
from tool.Pickler import Pickler


class Manager:
	def __init__(self):
		self.idx = 0
		self.unverified = []
		self.verified = []

	def get_list(self, offline=True):
		if offline:
			self.unverified = Pickler.load_obj('test_list')
			return self.unverified
		else:
			for i in range(1, 100):
				print(i)
				headers = {'Authorization': '127ae28c3362490c94e16d337a103f70'}
				res = requests.get(
					'https://newsapi.org/v2/everything?domains=cnn.com&language=en&page=' + str(i), headers=headers
				).json()

				for article in res['articles']:
					self.unverified.append({'title': article['title'], 'url': article['url']})

			Pickler.save_obj(self.unverified, 'test_list')
			return self.unverified

	def get_next(self):
		self.idx += 1
		if len(self.unverified) > self.idx:
			return self.unverified[self.idx]['title']
		else:
			return 'end of the list reached!'

	def set_result(self, res):
		url = self.unverified[self.idx]['url']
		title = self.unverified[self.idx]['title']
		self.verified.append({'url': url, 'title': title, 'label': res})

	#  Makes sure there are no duplicates in that massive, annoying list
	#  should be run before writing out our list
	def clear_duplicates(self):
		for thing in self.verified:
			print(thing)
			pass  # todo: do it

	def write_out_list(self):
		self.clear_duplicates()
		Pickler.save_obj(self.verified, 'verified_training_set')
