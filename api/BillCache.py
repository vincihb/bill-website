from db.SqlExecutor import SqlExecutor


class BillCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_meta_data(self, meta_data):
        pass

    def store_data(self, data_dict):
        sql = 'INSERT INTO `BILLS` (BILL_ID, TITLE, CONGRESS_SESSION, INTRODUCED_DATE, ACTIVE) VALUES (?, ?, ?)'
        pass

    def check_cache(self, bill_id):
        pass