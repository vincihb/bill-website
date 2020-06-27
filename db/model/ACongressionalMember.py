from db.model.APolitician import APolitician

"""
    Abstract Congressional Member class that helps reduce duplication of effort across
    Senate and House member classes
"""


class ACongressionalMember(APolitician):
    CSPAN_ID = None
    ICPSR_ID = None
    CRP_ID = None
    FEC_CANDIDATE_ID = None
    IN_OFFICE = None
    SENIORITY = None
    TOTAL_VOTES = None
    MISSED_VOTES = None
    TOTAL_PRESENT = None
    OFFICE = None
    PHONE = None
    FAX = None
    STATE = None
    MISSED_VOTES_PCT = None
    VOTES_WITH_PARTY_PCT = None

    def set_common_member_fields(self, db_object):
        self.set_common_politician_fields(db_object)

        self.CSPAN_ID = db_object.get('CSPAN_ID')
        self.ICPSR_ID = db_object.get('ICPSR_ID')
        self.CRP_ID = db_object.get('CRP_ID')
        self.FEC_CANDIDATE_ID = db_object.get('FEC_CANDIDATE_ID')
        self.IN_OFFICE = db_object.get('IN_OFFICE')
        self.SENIORITY = db_object.get('SENIORITY')
        self.TOTAL_VOTES = db_object.get('TOTAL_VOTES')
        self.MISSED_VOTES = db_object.get('MISSED_VOTES')
        self.TOTAL_PRESENT = db_object.get('TOTAL_PRESENT')
        self.OFFICE = db_object.get('OFFICE')
        self.PHONE = db_object.get('PHONE')
        self.FAX = db_object.get('FAX')
        self.STATE = db_object.get('STATE')
        self.MISSED_VOTES_PCT = db_object.get('MISSED_VOTES_PCT')
        self.VOTES_WITH_PARTY_PCT = db_object.get('VOTES_WITH_PARTY_PCT')

    def get_base_member_dict(self):
        data_dict = self.get_base_politician_dict()
        data_dict['cspan_id'] = self.CSPAN_ID
        data_dict['icpsr_id'] = self.ICPSR_ID
        data_dict['crp_id'] = self.CRP_ID
        data_dict['fec_candidate_id'] = self.FEC_CANDIDATE_ID
        data_dict['in_office'] = self.IN_OFFICE
        data_dict['seniority'] = self.SENIORITY
        data_dict['total_votes'] = self.TOTAL_VOTES
        data_dict['missed_votes'] = self.MISSED_VOTES
        data_dict['total_present'] = self.TOTAL_PRESENT
        data_dict['office'] = self.OFFICE
        data_dict['phone'] = self.PHONE
        data_dict['fax'] = self.FAX
        data_dict['state'] = self.STATE
        data_dict['missed_votes_pct'] = self.MISSED_VOTES_PCT
        data_dict['votes_with_party_pct'] = self.VOTES_WITH_PARTY_PCT
        return data_dict
