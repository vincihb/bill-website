from server.bill.bill_cilent import bill_client_routes
from server.bill.bill_api import bill_api_routes


def all_bill_routes(app):
    bill_client_routes(app)
    bill_api_routes(app)
