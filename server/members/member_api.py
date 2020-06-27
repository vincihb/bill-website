import json

from api.propublica.MemberCache import MemberCache


def member_api_routes(app):
    @app.route("/api/member/<string:member_id>", methods=['GET'])
    def get_member_api(member_id):
        member = MemberCache().get_house_member_by_id(member_id)
        if member is None:
            member = MemberCache().get_senate_member_by_id(member_id)

        if member is None:
            return json.dumps({'success': False})

        return json.dumps(
            {'success': True, 'data': {'first_name': member['FIRST_NAME'], 'last_name': member['LAST_NAME']}}
        )