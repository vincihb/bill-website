from db.SqlExecutor import SqlExecutor


class CongressCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_congress_session(self, session_num, start_date, end_date):
        sql = 'INSERT INTO `CONGRESSIONAL_SESSION` (NUMBER, START_DATE, END_DATE) ' \
              'VALUES(?, ?, ?)'
        self.db.exec_insert(sql, (session_num, start_date, end_date))

    def get_all_congress_session(self):
        sql = 'SELECT * FROM `CONGRESSIONAL_SESSION`'
        result = self.db.exec_select(sql).fetchall()
        return result

    # Check if congressional_session indeed has information about a specific session
    def get_congress_session(self, session_num):
        sql = 'SELECT * FROM `CONGRESSIONAL_SESSION` WHERE NUMBER=?'
        result = self.db.exec_select(sql, (session_num,)).fetchone()
        return result
