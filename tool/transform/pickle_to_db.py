from tool.Pickler import Pickler
from api.propublica.PropublicaScraper import PropublicaScraper
from os import path
from api.propublica.CongressCache import CongressCache
from api.propublica.PresidentCache import PresidentCache
from db.SqlExecutor import SqlExecutor
import json
import datetime as dt


class PickleToDB:
    def __init__(self, pickle_file):
        self.pickler = Pickler()
        self.congress_cache = CongressCache()
        self.president_cache = PresidentCache()
        self.sqlEx = SqlExecutor()
        self.pickle_file = pickle_file
        self.local_dir = path.dirname(path.abspath(__file__))

    def populate_president_cache(self):
        object_path = path.join(self.local_dir, '..', '..', 'data', 'json_files', 'presidents.json')
        with open(object_path) as json_file:
            data = json.load(json_file)
            for pres in data:
                if pres['left_office'] is not None:
                    left_office_date = dt.datetime.strptime(pres['left_office'], '%Y-%m-%d').date().toordinal()
                else:
                    left_office_date = None
                if self.president_cache.get_president_by_num(pres['number']) is None:
                    self.president_cache.store_president(pres['number'], pres['president'], pres['birth_year'],
                                                         pres['death_year'],
                                                         dt.datetime.strptime(pres['took_office'],
                                                                              '%Y-%m-%d').date().toordinal(),
                                                         left_office_date,
                                                         pres['party'])

    def populate_congressional_sessions(self):
        session_number = 1
        year = 1789
        while year <= dt.datetime.today().year:
            if self.congress_cache.get_congress_session(session_number) is None:
                if session_number < 73:
                    self.congress_cache.store_congress_session(session_number,
                                                               dt.datetime.strptime(str(year) + '-03-04',
                                                                                    '%Y-%m-%d').toordinal(),
                                                               dt.datetime.strptime(str(year + 2) + '-03-03',
                                                                                    '%Y-%m-%d').toordinal())
                elif session_number == 73:
                    self.congress_cache.store_congress_session(session_number,
                                                               dt.datetime.strptime(str(year) + '-03-04',
                                                                                    '%Y-%m-%d').toordinal(),
                                                               dt.datetime.strptime(str(year + 3) + '-01-03',
                                                                                    '%Y-%m-%d').toordinal())
                else:
                    self.congress_cache.store_congress_session(session_number,
                                                               dt.datetime.strptime(str(year) + '-01-02',
                                                                                    '%Y-%m-%d').toordinal(),
                                                               dt.datetime.strptime(str(year + 2) + '-01-03',
                                                                                    '%Y-%m-%d').toordinal())
            year = year + 2
            session_number = session_number + 1

    def populate_president_to_session(self):
        president_number = 1
        session_number = 1
        while True:
            president_data = self.president_cache.get_president_by_num(president_number)
            session_data = self.congress_cache.get_congress_session(session_number)
            if session_data is None or president_data is None:
                break
            president_start_date = president_data[4]
            president_end_date = president_data[5]
            session_start_date = session_data[1]
            session_end_date = session_data[2]
            if president_end_date is None:
                president_end_date = dt.datetime.today().toordinal()
            if president_start_date <= session_start_date <= president_end_date <= session_end_date:
                if self.president_cache.check_president_session_cache(president_number, session_number) is None:
                    self.president_cache.store_president_session(session_number, president_number)
                president_number = president_number + 1
            elif session_end_date >= president_start_date:
                if self.president_cache.check_president_session_cache(president_number, session_number) is None:
                    self.president_cache.store_president_session(session_number, president_number)
                session_number = session_number + 1
            else:
                print("Wait this should work!")

    def pickle_to_db(self):
        object_path = path.join(self.local_dir, '..', '..', 'obj', 'complete', self.pickle_file)
        members = self.pickler.load_obj(object_path)
        for keys in members:
            print(members[keys])
            # for member_keys in members[keys]:
            #     exit()


if __name__ == "__main__":
    transform = PickleToDB('House Members.pkl')
    # transform.pickle_to_db()
    # exit()
    transform.populate_president_cache()
    transform.populate_congressional_sessions()
    transform.populate_president_to_session()
    print(transform.president_cache.get_session_from_president(45))
    print(transform.president_cache.get_president_by_num(45))
    a = transform.congress_cache.get_congress_session(116)
    print(dt.datetime.fromordinal(a[2]))
