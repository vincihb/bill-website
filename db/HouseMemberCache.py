from db.AMemberCache import AMemberCache


class HouseMemberCache(AMemberCache):
    def __init__(self):
        super().__init__()
        self._setup('HOUSE_MEMBER', 'HOUSE_MEMBER_TO_SESSION')

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
        self._db.exec_insert(sql, (id, first_name, mid_name, last_name, dob, gender, party,
                                  leadership_role, twitter_account, facebook_account, youtube_account,
                                  cspan_id, icpsr_id, crp_id, fec_candidate_id, in_office, seniority,
                                  total_votes, missed_votes, total_present, office, phone, fax, state,
                                  district, at_large, missed_votes_pct,
                                  votes_with_party_pct))
        # Note, make sure that the member_data is a tuple and that it is structured properly in the order as above

    def store_house_member_to_session(self, session_num, member_id):
        return self.store_member_to_session(session_num, member_id)

    def get_house_member_by_id(self, member_id):
        return self.get_by_id(member_id)

    def get_session_from_house_member_id(self, member_id):
        return self.get_session_by_id(member_id)
