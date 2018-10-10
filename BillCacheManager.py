from threading import Thread, active_count, current_thread
import asyncio

class BillCacheManager:

	def __init__(self):
		pass

	def start(self):
		c_t_i = current_thread()
		print(c_t_i.getName())

	def get_recent_bills(self):
		pass

	def get_popular_bills(self):
		pass

	def cache(self, batch: list):
		pass


print(active_count())
t = Thread(target=BillCacheManager().start, name="Async Bill Caching Thread")
t.start()


c_t = current_thread()
print(c_t.getName())
print(t.getName())
print(active_count())
