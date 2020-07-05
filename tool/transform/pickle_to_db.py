from tool.Pickler import Pickler
from os import path
from db.CongressCache import CongressCache
from db.PresidentCache import PresidentCache
from db.HouseMemberCache import HouseMemberCache
from db.SenateMemberCache import SenateMemberCache
from db.BillCache import BillCache
from db.SqlExecutor import SqlExecutor
import json
import datetime as dt


class PickleToDB:
    def __init__(self, pickle_file):
        self.pickler = Pickler()
        self.congress_cache = CongressCache()
        self.president_cache = PresidentCache()
        self.house_member_cache = HouseMemberCache()
        self.senate_member_cache = SenateMemberCache()
        self.bill_cache = BillCache()
        self.sqlEx = SqlExecutor()
        self.pickle_file = pickle_file
        self.local_dir = path.dirname(path.abspath(__file__))
        if self.pickle_file == 'House Members.pkl':
            self.congressional_body = 'House'
        else:
            self.congressional_body = 'Senate'

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
            president_start_date = president_data['TOOK_OFFICE']
            president_end_date = president_data['LEFT_OFFICE']
            session_start_date = session_data['START_DATE']
            session_end_date = session_data['END_DATE']
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

    def populate_members_cache(self):
        object_path = path.join(self.local_dir, '..', '..', 'obj', 'complete', self.pickle_file)
        members = self.pickler.load_obj(object_path)
        for keys in members:
            member = members[keys]

            date_of_birth_string = member.get('date_of_birth')
            if date_of_birth_string != '':
                date_of_birth = dt.datetime.strptime(date_of_birth_string, '%Y-%m-%d').toordinal()
            else:
                date_of_birth = 0

            if self.congressional_body is 'House':
                if self.house_member_cache.get_house_member_by_id(member['id']) is None:
                    self.house_member_cache.store_house_member(member.get('id'), member.get('first_name'),
                                                               member.get('middle_name'), member.get('last_name'),
                                                               date_of_birth,
                                                               member.get('gender'), member.get('party'),
                                                               member.get('leadership_role'), member.get('twitter_account'),
                                                               member.get('facebook_account'), member.get('youtube_account'),
                                                               member.get('cspan_id'), member.get('icpsr_id'),
                                                               member.get('crp_id'), member.get('fec_candidate_id'),
                                                               member.get('in_office'), member.get('seniority'),
                                                               member.get('total_votes'), member.get('missed_votes'),
                                                               member.get('total_present'), member.get('office'),
                                                               member.get('phone'), member.get('fax'),
                                                               member.get('state'), member.get('district'),
                                                               member.get('at_large'), member.get('missed_votes_pct'),
                                                               member.get('votes_with_party_pct'))
            else:
                if self.senate_member_cache.get_senate_member_by_id(member['id']) is None:
                    self.senate_member_cache.store_senate_member(member.get('id'), member.get('first_name'),
                                                                member.get('middle_name'), member.get('last_name'),
                                                                date_of_birth, member.get('gender'), member.get('party'),
                                                                member.get('leadership_role'), member.get('twitter_account'),
                                                                member.get('facebook_account'), member.get('youtube_account'),
                                                                member.get('cspan_id'), member.get('icpsr_id'),
                                                                member.get('crp_id'), member.get('fec_candidate_id'),
                                                                member.get('in_office'), member.get('seniority'),
                                                                member.get('total_votes'), member.get('missed_votes'),
                                                                member.get('total_present'), member.get('office'),
                                                                member.get('phone'), member.get('fax'), member.get('state'),
                                                                member.get('senate_class'), member.get('state_rank'))

    def populate_members_to_session(self):
        object_path = path.join(self.local_dir, '..', '..', 'obj', 'complete', self.pickle_file)
        members = self.pickler.load_obj(object_path)
        for key in members:
            member = members[key]
            member_id = member['id']
            first_session = member['last_session']
            last_session = member['first_session']
            if self.congressional_body is 'House':
                if len(self.house_member_cache.get_session_from_house_member_id(member_id)) == (last_session - first_session) + 1:
                    continue

                for session_num in range(first_session, last_session + 1):
                    self.house_member_cache.store_house_member_to_session(session_num, member_id)
            else:
                if len(self.senate_member_cache.get_session_from_senate_member_id(member_id)) == (last_session - first_session) + 1:
                    continue

                for session_num in range(first_session, last_session + 1):
                    self.senate_member_cache.store_senate_member_to_session(session_num, member_id)

    def populate_bill_cache(self):
        object_path = path.join(self.local_dir, '..', '..', 'obj', 'complete', self.pickle_file)
        bills = self.pickler.load_obj(object_path)
        for key in bills:
            bill = bills[key]
            vetoed = True
            if bill.get('latest_major_action') != 'Received in the Senate.' and bill.get('enacted') is None:
                enacted = False
            else:
                enacted = True
            if bill.get('vetoed') is None:
                vetoed = False
            congress_session = int(bill['bill_id'][len(bill['bill_id']) - 3: len(bill['bill_id'])])
            self.bill_cache.store_bill(bill.get('bill_id'), bill['title'], bill.get('short_title'), congress_session,
                                       dt.datetime.strptime(bill.get('introduced_date'), '%Y-%m-%d').toordinal(),
                                       bill.get('congressdotgov_url'), bill.get('active'),
                                       enacted, vetoed, bill.get('summary'), bill.get('latest_major_action'))


if __name__ == "__main__":
    transform = PickleToDB('House Members.pkl')
    print("Populating president's cache")
    transform.populate_president_cache()
    print("Populating congressional sessions")
    transform.populate_congressional_sessions()
    print("Linking presidents to sessions")
    transform.populate_president_to_session()
    print("Populating house members")
    transform.populate_members_cache()
    transform.populate_members_to_session()
    print("Populating senate members")
    transform = PickleToDB('Senate Members.pkl')
    transform.populate_members_cache()
    transform.populate_members_to_session()
    print("Populating bill set")
    for i in range(105, 117):
        print(str(i))
        transform = PickleToDB('Bill Set-' + str(i) + '-Complete.pkl')
        transform.populate_bill_cache()
    # test = transform.member_cache.get_house_member_from_session(115)
    # print(test)
    # print(len(test))
