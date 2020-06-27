from db.SqlExecutor import SqlExecutor


class HouseMemberCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_house_member(self,
                              id, first_name, mid_name, last_name, dob, gender, party,
                              leadership_role, twitter_account, facebook_account, youtube_account,
                              cspan_id, icpsr_id, crp_id, fec_candidate_id, in_office, seniority,
                              total_votes, missed_votes, total_present, office, phone, fax, state,
                              district, at_large, missed_votes_pct,
                              votes_with_party_pct):
        sql = 'INSERT INTO `HOUSE_MEMBER` (ID, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DATE_OF_BIRTH,' \
              'GENDER, PARTY, LEADERSHIP_ROLE, TWITTER_ACCOUNT, FACEBOOK_ACCOUNT, YOUTUBE_ACCOUNT, CSPAN_ID, ' \
              'ICPSR_ID, CRP_ID, FEC_CANDIDATE_ID, IN_OFFICE, SENIORITY, TOTAL_VOTES, MISSED_VOTES, ' \
              'TOTAL_PRESENT, OFFICE, PHONE, FAX, STATE, DISTRICT, AT_LARGE, ' \
              'MISSED_VOTES_PCT, VOTES_WITH_PARTY_PCT) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.db.exec_insert(sql, (id, first_name, mid_name, last_name, dob, gender, party,
                                  leadership_role, twitter_account, facebook_account, youtube_account,
                                  cspan_id, icpsr_id, crp_id, fec_candidate_id, in_office, seniority,
                                  total_votes, missed_votes, total_present, office, phone, fax, state,
                                  district, at_large, missed_votes_pct,
                                  votes_with_party_pct))
        # Note, make sure that the member_data is a tuple and that it is structured properly in the order as above

    def store_house_member_to_session(self, session_num, member_id):
        sql = 'INSERT INTO `HOUSE_MEMBER_TO_SESSION` (SESSION_NUMBER, MEMBER_ID) VALUES(?, ?)'
        self.db.exec_insert(sql, (session_num, member_id))

    def get_all_house_members_data(self):
        sql = 'SELECT * FROM `HOUSE_MEMBER`'
        result = self.db.exec_select(sql).fetchall()
        return result

    def get_house_member_by_id(self, member_id):
        sql = 'SELECT * FROM `HOUSE_MEMBER` WHERE ID=?'
        result = self.db.exec_select(sql, (member_id,)).fetchone()
        return result

    def get_house_member_last_name(self, member_last_name):
        sql = 'SELECT * FROM `HOUSE_MEMBER` WHERE LAST_NAME=?'
        result = self.db.exec_select(sql, (member_last_name,)).fetchall()
        return result

    def get_house_member_first_name(self, member_first_name):
        sql = 'SELECT * FROM `HOUSE_MEMBER` WHERE FIRST_NAME=?'
        result = self.db.exec_select(sql, (member_first_name,)).fetchall()
        return result

    def get_house_member_district_name(self, district):
        sql = 'SELECT * FROM `HOUSE_MEMBER` WHERE DISTRICT=?'
        result = self.db.exec_select(sql, (district,)).fetchall()
        return result

    def get_house_member_from_session(self, session_number):
        sql = 'SELECT * FROM `HOUSE_MEMBER_TO_SESSION` INNER JOIN `HOUSE_MEMBER` ON ' \
              '`HOUSE_MEMBER_TO_SESSION`.MEMBER_ID=`HOUSE_MEMBER`.ID ' \
              'WHERE SESSION_NUMBER=?'
        result = self.db.exec_select(sql, (session_number,)).fetchall()
        return result

    def get_session_from_house_member_id(self, member_id):
        sql = 'SELECT * FROM `HOUSE_MEMBER_TO_SESSION` INNER JOIN `CONGRESSIONAL_SESSION` ON ' \
              '`HOUSE_MEMBER_TO_SESSION`.SESSION_NUMBER=`CONGRESSIONAL_SESSION`.NUMBER ' \
              'WHERE MEMBER_ID=?'
        result = self.db.exec_select(sql, (member_id,)).fetchall()
        return result


