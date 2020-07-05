from db.model.ACongressionalMember import ACongressionalMember
from db.HouseMemberCache import HouseMemberCache


class HouseMember(ACongressionalMember):
    DISTRICT = None
    AT_LARGE = None

    def __init__(self):
        self._table = ''

    def save(self):
        pass

    def get(self, _id):
        pass

    def as_dict(self):
        data = self.get_base_member_dict()
        data['district'] = self.DISTRICT
        data['at_large'] = self.AT_LARGE
        return data

    def _from_db(self, db_row):
        self.set_common_member_fields(db_row)
        self.DISTRICT = db_row["DISTRICT"]
        self.AT_LARGE = db_row["AT_LARGE"]

    @staticmethod
    def get_all():
        all_structured_members = []
        all_members = HouseMemberCache().get_all()
        for member in all_members:
            all_structured_members.append(HouseMember.from_db(member).as_dict())

        return all_structured_members

    @staticmethod
    def from_db(db_object):
        hm = HouseMember()
        hm._from_db(db_object)
        return hm
