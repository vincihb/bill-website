from db.SqlExecutor import SqlExecutor


class MemberCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_congress_member(self,
                              id, first_name, mid_name, last_name, gender, party,
                              leadership_role, twitter_account, facebook_account, youtube_account,
                              cspan_id, icpsr_id, crp_id, fec_candidate_id, in_office, seniority,
                              total_votes, missed_votes, total_present, office, phone, fax, state,
                              district, at_large, senate_class, state_rank, missed_votes_pct,
                              votes_with_party_pct, title, session):
        sql = 'INSERT INTO `MEMBER` (ID, FIRST_NAME, MIDDLE_NAME, LAST_NAME, GENDER, PARTY, ' \
              'LEADERSHIP_ROLE, TWITTER_ACCOUNT, FACEBOOK_ACCOUNT, YOUTUBE_ACCOUNT, CSPAN_ID, ' \
              'ICPSR_ID, CRP_ID, FEC_CANDIDATE_ID, IN_OFFICE, SENIORITY, TOTAL_VOTES, MISSED_VOTES, ' \
              'TOTAL_PRESENT, OFFICE, PHONE, FAX, STATE, DISTRICT, AT_LARGE, SENATE_CLASS, ' \
              'STATE_RANK, MISSED_VOTES_PCT, VOTES_WITH_PARTY_PCT, TITLE, SESSION) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.db.exec_insert(sql, (id, first_name, mid_name, last_name, gender, party,
                              leadership_role, twitter_account, facebook_account, youtube_account,
                              cspan_id, icpsr_id, crp_id, fec_candidate_id, in_office, seniority,
                              total_votes, missed_votes, total_present, office, phone, fax, state,
                              district, at_large, senate_class, state_rank, missed_votes_pct,
                              votes_with_party_pct, title, session))
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