from threading import Thread, active_count
from api.PropublicaScraper import PropublicaScraper


class BillCacheManager:
    @staticmethod
    def start():
        print(active_count())
        t = Thread(target=BillCacheManager().refresh_cache, name="Async Bill Caching Thread")
        t.start()

    @staticmethod
    def refresh_cache():
        print('Refresh the cache man!')
        PropublicaScraper.get_bills_for_session(116)
