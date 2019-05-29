import json
from Pickler import Pickler


# Used to repair data where Propublica returns broken data
class BillDataRepairer():
    # read data back out to a temp pickle file
    @staticmethod
    def reload_bill_json(session, offset):
        with open('z_tmp_json.json') as j:
            data = json.load(j)
            session_bills = dict()
            for bill in data['results'][0]['bills']:
                bill_id = bill['bill_id']
                session_bills[bill_id] = bill

            Pickler.save_obj(session_bills, str(session) + '-' + str(offset))

    @staticmethod
    def merger(session, merge_set):
        main = Pickler.load_obj('Bill Set-' + str(session) + '-3')
        for subset in merge_set:
            print(subset)
            sub = Pickler.load_obj(str(session) + '-' + subset)
            for bill in sub:
                main[bill] = sub[bill]

        Pickler.save_obj(main, 'Bill Set-' + str(session) + '-Complete')