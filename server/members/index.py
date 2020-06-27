from server.members.member_cilent import member_client_routes
from server.members.member_api import member_api_routes


def all_member_routes(app):
    member_client_routes(app)
    member_api_routes(app)
