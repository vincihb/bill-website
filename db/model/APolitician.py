from db.model.ADBItem import ADBItem

"""
    Abstract Politician class that can be extended as needed
"""


class APolitician(ADBItem):
    FIRST_NAME = None
    MIDDLE_NAME = None
    LAST_NAME = None
    DATE_OF_BIRTH = None
    GENDER = None
    PARTY = None
    LEADERSHIP_ROLE = None
    TWITTER_ACCOUNT = None
    FACEBOOK_ACCOUNT = None
    YOUTUBE_ACCOUNT = None

    def set_common_politician_fields(self, db_object):
        self.FIRST_NAME = db_object.get('FIRST_NAME')
        self.MIDDLE_NAME = db_object.get('MIDDLE_NAME')
        self.LAST_NAME = db_object.get('LAST_NAME')
        self.DATE_OF_BIRTH = db_object.get('DATE_OF_BIRTH')
        self.GENDER = db_object.get('GENDER')
        self.PARTY = db_object.get('PARTY')
        self.LEADERSHIP_ROLE = db_object.get('LEADERSHIP_ROLE')
        self.TWITTER_ACCOUNT = db_object.get('TWITTER_ACCOUNT')
        self.FACEBOOK_ACCOUNT = db_object.get('FACEBOOK_ACCOUNT')
        self.YOUTUBE_ACCOUNT = db_object.get('YOUTUBE_ACCOUNT')

    def get_base_politician_dict(self):
        return {
            'first_name': self.FIRST_NAME,
            'middle_name': self.MIDDLE_NAME,
            'last_name': self.LAST_NAME,
            'date_of_birth': self.DATE_OF_BIRTH,
            'gender': self.GENDER,
            'party': self.PARTY,
            'leadership_role': self.LEADERSHIP_ROLE,
            'twitter_account': self.TWITTER_ACCOUNT,
            'facebook_account': self.FACEBOOK_ACCOUNT,
            'youtube_account': self.YOUTUBE_ACCOUNT
        }
