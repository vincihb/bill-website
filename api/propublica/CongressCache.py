from db.SqlExecutor import SqlExecutor


class CongressCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_congress_member(self, member_data):
        sql = 'INSERT INTO `MEMBER` (ID, FIRST_NAME, MIDDLE_NAME, LAST_NAME, GENDER, PARTY, ' \
              'LEADERSHIP_ROLE, TWITTER_ACCOUNT, FACEBOOK_ACCOUNT, YOUTUBE_ACCOUNT, CSPAN_ID, ' \
              'ICPSR_ID, CRP_ID, FEC_CANDIDATE_ID, IN_OFFICE, SENIORITY, TOTAL_VOTES, MISSED_VOTES, ' \
              'TOTAL_PRESENT, OFFICE, PHONE, FAX, STATE, DISTRICT, AT_LARGE, SENATE_CLASS, ' \
              'STATE_RANK, MISSED_VOTES_PCT, VOTES_WITH_PARTY_PCT, TITLE, SESSION) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.db.exec_insert(sql, member_data)
        # Note, make sure that the member_data is a tuple and that it is structured properly in the order as above

    def get_all_congress_members_data(self):
        sql = 'SELECT * FROM `MEMBER`'
        result = self.db.exec_select(sql).fetchall()
        return result

    def get_congress_member(self, member_id):
        sql = 'SELECT * FROM `MEMBER` WHERE ID=?'
        result = self.db.exec_select(sql, (member_id,)).fetchone()
        return result

    def get_all_congress_sessions_for_member(self, member_id):
        sql = 'SELECT * FROM `MEMBER` INNER JOIN CONGRESSIONAL_SESSION ON ' \
              '`MEMBER`.SESSION=`CONGRESSIONAL_SESSION`.NUMBER WHERE ID=?'
        result = self.db.exec_select(sql, (member_id,)).fetchall()
        return result

    def store_congress_session(self, session_num, president, start_date, end_date):
        sql = 'INSERT INTO `CONGRESSIONAL_SESSION` (NUMBER, PRESIDENT, START_DATE, END_DATE) ' \
              'VALUES(?, ?, ?, ?)'
        self.db.exec_insert(sql, (session_num, president, start_date, end_date))

    def get_all_congress_session(self):
        sql = 'SELECT * FROM `CONGRESSIONAL_SESSION`'
        result = self.db.exec_select(sql).fetchall()
        return result

    # Check if congressional_session indeed has information about a specific session
    def get_congress_session(self, session_num):
        sql = 'SELECT * FROM `CONGRESSIONAL_SESSION` WHERE NUMBER=?'
        result = self.db.exec_select(sql, (session_num,)).fetchone()
        return result
