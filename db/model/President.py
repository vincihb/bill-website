from db.model.APolitician import APolitician


class President(APolitician):
    def __init__(self):
        pass

    def save(self):
        pass

    def get(self, _id):
        pass

    def as_dict(self):
        return self.get_base_politician_dict()

    def _from_db(self, db_row):
        self.set_common_politician_fields(db_row)

    @staticmethod
    def from_db(db_object):
        president = President()
        president._from_db(db_object)
        return president
