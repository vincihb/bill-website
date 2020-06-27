from db.SqlExecutor import SqlExecutor


class PresidentCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_president(self, number, name, birth_year, death_year, took_office, left_office, party):
        sql = 'INSERT INTO `PRESIDENT` (NUMBER, NAME, BIRTH_YEAR, DEATH_YEAR, TOOK_OFFICE, LEFT_OFFICE, PARTY)' \
          'VALUES(?, ?, ?, ?, ?, ?, ?)'
        self.db.exec_insert(sql, (number, name, birth_year, death_year, took_office, left_office, party))

    def get_president_by_num(self, number):
        sql = 'SELECT * FROM `PRESIDENT` WHERE NUMBER=?'
        result = self.db.exec_select(sql, (number,)).fetchone()
        return result

    def store_president_session(self, session_number, president_number):
        sql = 'INSERT INTO `PRESIDENT_TO_SESSION` (SESSION_NUMBER, PRESIDENT_NUMBER) VALUES(?, ?)'
        self.db.exec_insert(sql, (session_number, president_number))

    def get_president_from_session(self, session_number):
        sql = 'SELECT * FROM `PRESIDENT_TO_SESSION` INNER JOIN `PRESIDENT` ON ' \
              '`PRESIDENT_TO_SESSION`.PRESIDENT_NUMBER=`PRESIDENT`.NUMBER ' \
              'WHERE SESSION_NUMBER=?'
        result = self.db.exec_select(sql, (session_number,)).fetchall()
        return result

    def get_session_from_president(self, president_number):
        sql = 'SELECT * FROM `PRESIDENT_TO_SESSION` INNER JOIN `CONGRESSIONAL_SESSION` ON ' \
              '`PRESIDENT_TO_SESSION`.SESSION_NUMBER=`CONGRESSIONAL_SESSION`.NUMBER ' \
              'WHERE PRESIDENT_NUMBER=?'
        result = self.db.exec_select(sql, (president_number,)).fetchall()
        return result

    def check_president_session_cache(self, president_number, session_number):
        sql = 'SELECT * FROM `PRESIDENT_TO_SESSION` WHERE PRESIDENT_NUMBER=? AND SESSION_NUMBER=?'
        result = self.db.exec_select(sql, (president_number, session_number)).fetchone()
        return result

