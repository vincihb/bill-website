from db.SqlExecutor import SqlExecutor
from db.CongressCache import CongressCache


class BillCache:
    def __init__(self):
        self.db = SqlExecutor()
        self.congress_cache = CongressCache()

    def store_keyword_to_bill(self, key_word, bill_data, weight):
        sql = 'INSERT INTO `BILL_KEYWORDS` (KEYWORD, BILL_ID, WEIGHT)'
        self.db.exec_insert(sql, (key_word, bill_data, weight))

    def store_bill(self, id, title, short_title, congress_session, intro_date, bill_url, active,
                   enacted, vetoed, summary, latest_major_action):
        sql = 'INSERT INTO `BILL` (ID, TITLE, SHORT_TITLE,' \
              'CONGRESS_SESSION, INTRODUCED_DATE, BILL_URL,' \
              'ACTIVE, ENACTED, VETOED, SUMMARY, LATEST_MAJOR_ACTION) VALUES (?, ?, ?, ?, ?, ' \
              '?, ?, ?, ?, ?, ?)'
        self.db.exec_insert(sql, (id, title, short_title, congress_session, intro_date, bill_url, active,
                   enacted, vetoed, summary, latest_major_action))
        # Note: make sure data is in tuple form

    def get_all_bills(self):
        sql = 'SELECT * FROM `BILL`'
        result = self.db.exec_select(sql).fetchall()
        return result

    def get_bill_from_session(self, session):
        sql = 'SELECT * FROM `BILL` WHERE CONGRESS_SESSION=?'
        result = self.db.exec_select(sql, (session, )).fetchall()
        return result

    def get_bill_from_bill_id(self, bill_id):
        sql = 'SELECT * FROM `BILL` WHERE BILL_ID=?'
        result = self.db.exec_select(sql, (bill_id,)).fetchone()
        return result

    def get_all_cosponsors_for_bill(self, bill_id):
        sql = 'SELECT * FROM `COSPONSOR` INNER JOIN `MEMBER` ON `COSPONSOR`.MEMBER_ID=`MEMBER`.ID WHERE BILL_ID=?'
        result = self.db.exec_select(sql, (bill_id,)).fetchall()
        return result

    def get_all_cosponsored_bills_for_member(self, member_id):
        sql = 'SELECT * FROM `COSPONSOR` INNER JOIN `BILL` ON `COSPONSOR`.BILL_ID=`BILL`.ID WHERE MEMBER_ID=?'
        result = self.db.exec_select(sql, (member_id,)).fetchall()
        return result

    def check_cache(self, bill_id):
        session_num = int(bill_id[len(bill_id) - 3: len(bill_id)])
        result = self.congress_cache.get_congress_session(session_num)
        if result is not None:
            return self.get_bill(bill_id)
        return None  # If no metadata found due to congressional_session, then bill is not there
