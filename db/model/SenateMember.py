from db.model.ACongressionalMember import ACongressionalMember


class SenateMember(ACongressionalMember):
    SENATE_RANK = None
    SENATE_CLASS = None

    def __init__(self):
        pass

    def save(self):
        pass

    def get(self, _id):
        pass

    def as_dict(self):
        data = self.get_base_member_dict()
        data['senate_class'] = self.SENATE_CLASS
        data['senate_rank'] = self.SENATE_RANK
        return data

    def _from_db(self, db_row):
        self.set_common_member_fields(db_row)
        self.SENATE_CLASS = db_row["SENATE_CLASS"]
        self.SENATE_RANK = db_row["SENATE_RANK"]
        return self

    @staticmethod
    def from_db(db_object):
        sm = SenateMember()
        sm._from_db(db_object)
        return sm
