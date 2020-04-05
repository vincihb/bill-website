from db.SqlExecutor import SqlExecutor
from api.propublica.CongressCache import CongressCache


class BillCache:
    def __init__(self):
        self.db = SqlExecutor()
        self.congress_cache = CongressCache()

    def store_keyword_to_bill(self, key_word, bill_data, weight):
        sql = 'INSERT INTO `BILL_KEYWORDS` (KEYWORD, BILL_ID, WEIGHT)'
        self.db.exec_insert(sql, (key_word, bill_data, weight))

    def store_bill(self, data_tuple):
        sql = 'INSERT INTO `BILLS` (ID, TITLE, CONGRESS_SESSION, INTRODUCED_DATE, CONGRESS_URL, BILL_URL,' \
              'ACTIVE, BILL_ID, ENACTED, VETOED, SUMMARY, LATEST_MAJOR_ACTION) VALUES (?, ?, ?, ?, ?, ?, ' \
              '?, ?, ?, ?, ?, ?)'
        self.db.exec_insert(sql, data_tuple)
        # Note: make sure data is in tuple form

    def get_bill(self, bill_id):
        sql = 'SELECT * FROM `BILLS` WHERE BILL_ID=?'
        result = self.db.exec_select(sql, (bill_id,)).fetchone()
        return result

    def get_all_cosponsors_for_bill(self, bill_id):
        sql = 'SELECT * FROM `COSPONSOR` INNER JOIN `MEMBER` ON `COSPONSOR`.MEMBER_ID=`MEMBER`.ID WHERE BILL_ID=?'
        result = self.db.exec_select(sql, (bill_id,)).fetchall()
        return result

    def get_all_cosponsored_bills_for_member(self, member_id):
        sql = 'SELECT * FROM `COSPONSOR` INNER JOIN `BILL` ON `COSPONSOR`.BILL_ID=`BILL`.ID WHERE MEMBER_ID=?';
        result = self.db.exec_select(sql, (member_id,)).fetchall()
        return result

    def check_cache(self, bill_id):
        session_num = int(bill_id[len(bill_id) - 3: len(bill_id)])
        result = self.congress_cache.get_congress_session(session_num)
        if result is not None:
            return self.get_bill(bill_id)
        return None  # If no metadata found due to congressional_session, then bill is not there
