from db.AMemberCache import AMemberCache


class SenateMemberCache(AMemberCache):
    def __init__(self):
        self._setup('SENATE_MEMBER', 'SENATE_MEMBER_TO_SESSION')

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
        self._db.exec_insert(sql, (id, first_name, mid_name, last_name, dob, gender, party,
                                   leadership_role, twitter_account, facebook_account, youtube_account,
                                   cspan_id, icpsr_id, crp_id, fec_candidate_id, in_office, seniority,
                                   total_votes, missed_votes, total_present, office, phone, fax, state,
                                   senate_class, state_rank))

    def store_senate_member_to_session(self, session_num, member_id):
        return self.store_member_to_session(session_num, member_id)

    def get_senate_member_by_id(self, member_id):
        return self.get_by_id(member_id)

    def get_session_from_senate_member_id(self, member_id):
        return self.get_session_by_id(member_id)
