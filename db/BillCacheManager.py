from threading import Thread, active_count
from api.propublica.ToPickle import ToPickle


class BillCacheManager:
    @staticmethod
    def start():
        print(active_count())
        t = Thread(target=BillCacheManager().refresh_cache, name="Async Bill Caching Thread")
        t.start()

    @staticmethod
    def refresh_cache():
        print('Refresh the cache man!')
        ToPickle.get_bills_for_session(116)
