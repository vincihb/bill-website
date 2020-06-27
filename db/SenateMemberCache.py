from db.SqlExecutor import SqlExecutor


class MemberCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_senate_member(self,
                            id, first_name, mid_name, last_name, dob, gender, party,
                            leadership_role, twitter_account, facebook_account, youtube_account,
                            cspan_id, icpsr_id, crp_id, fec_candidate_id, in_office, seniority,
                            total_votes, missed_votes, total_present, office, phone, fax, state
                            , senate_class, state_rank):
        sql = 'INSERT INTO `SENATE_MEMBER` (ID, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DATE_OF_BIRTH,' \
              'GENDER, PARTY, LEADERSHIP_ROLE, TWITTER_ACCOUNT, FACEBOOK_ACCOUNT, YOUTUBE_ACCOUNT, CSPAN_ID, ' \
              'ICPSR_ID, CRP_ID, FEC_CANDIDATE_ID, IN_OFFICE, SENIORITY, TOTAL_VOTES, MISSED_VOTES, ' \
              'TOTAL_PRESENT, OFFICE, PHONE, FAX, STATE, SENATE_CLASS, STATE_RANK) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.db.exec_insert(sql, (id, first_name, mid_name, last_name, dob, gender, party,
                                  leadership_role, twitter_account, facebook_account, youtube_account,
                                  cspan_id, icpsr_id, crp_id, fec_candidate_id, in_office, seniority,
                                  total_votes, missed_votes, total_present, office, phone, fax, state,
                                  senate_class, state_rank))

    def store_senate_member_to_session(self, session_num, member_id):
        sql = 'INSERT INTO `SENATE_MEMBER_TO_SESSION` (SESSION_NUMBER, MEMBER_ID) VALUES(?, ?)'
        self.db.exec_insert(sql, (session_num, member_id))

    def get_all_senate_members_data(self):
        sql = 'SELECT * FROM `SENATE_MEMBER`'
        result = self.db.exec_select(sql).fetchall()
        return result

    def get_senate_member_by_id(self, member_id):
        sql = 'SELECT * FROM `SENATE_MEMBER` WHERE ID=?'
        result = self.db.exec_select(sql, (member_id,)).fetchone()
        return result

    def get_senate_member_last_name(self, member_last_name):
        sql = 'SELECT * FROM `SENATE_MEMBER` WHERE LAST_NAME=?'
        result = self.db.exec_select(sql, (member_last_name,)).fetchall()
        return result

    def get_senate_member_first_name(self, member_first_name):
        sql = 'SELECT * FROM `SENATE_MEMBER` WHERE FIRST_NAME=?'
        result = self.db.exec_select(sql, (member_first_name,)).fetchall()
        return result

    def get_senate_member_from_session(self, session_number):
        sql = 'SELECT * FROM `SENATE_MEMBER_TO_SESSION` INNER JOIN `SENATE_MEMBER` ON ' \
              '`SENATE_MEMBER_TO_SESSION`.MEMBER_ID=`SENATE_MEMBER`.ID ' \
              'WHERE SESSION_NUMBER=?'
        result = self.db.exec_select(sql, (session_number,)).fetchall()
        return result

    def get_session_from_senate_member_id(self, member_id):
        sql = 'SELECT * FROM `SENATE_MEMBER_TO_SESSION` INNER JOIN `CONGRESSIONAL_SESSION` ON ' \
              '`SENATE_MEMBER_TO_SESSION`.SESSION_NUMBER=`CONGRESSIONAL_SESSION`.NUMBER ' \
              'WHERE MEMBER_ID=?'
        result = self.db.exec_select(sql, (member_id,)).fetchall()
        return result