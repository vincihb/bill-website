import json

from db.BillCache import BillCache
from db.Bill import Bill


def bill_api_routes(app):
    @app.route("/api/bill/<string:bill_id>", methods=['GET'])
    def get_bill_api(bill_id):
        bill = BillCache().get_bill(bill_id)
        if bill is None:
            return json.dumps({'success': False})

        data = {
            'success': True,
            'data': Bill.from_db(bill_id).get_json()
        }

        return json.dumps(data)
