import pandas as pd


class BillDataFrameBuilder:
    @staticmethod
    def build_from_list(bill_set, field_list) -> pd.DataFrame:
        contract = {
            'bill_id': '',
            'R': 0,
            'D': 0,
            'I': 0,
            'enacted': 0,
        }

        bill_id = 'bill_id'
        if bill_id not in field_list:
            field_list.append(bill_id)

        df = pd.DataFrame()
        for field in field_list:
            d = dict()
            if (field == 'sponsor_party'):
                BillDataFrameBuilder.append_sponsor_party(d, bill)



        return df

    @staticmethod
    def append_sponsor_party(d, bill):
        d['R'] = 1 if bill['sponsor_party'].lower() == 'r' else 0
        d['D'] = 1 if bill['sponsor_party'].lower() == 'd' else 0
        d['I'] = 0 if d['R'] == 1 or d['D'] == 1 else 1