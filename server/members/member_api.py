import json

from db.HouseMemberCache import HouseMemberCache
from db.SenateMemberCache import SenateMemberCache
from db.model.SenateMember import SenateMember
from db.model.HouseMember import HouseMember


def member_api_routes(app):
    @app.route("/api/member/<string:member_id>", methods=['GET'])
    def get_member_api(member_id):
        out_data = None
        house_member = HouseMemberCache().get_house_member_by_id(member_id)
        if house_member is not None:
            out_data = HouseMember.from_db(house_member).as_dict()
        else:
            senate_member = SenateMemberCache().get_senate_member_by_id(member_id)
            if senate_member is not None:
                out_data = SenateMember.from_db(senate_member).as_dict()

        if out_data is None:
            return json.dumps({'success': False})

        return json.dumps(
            {'success': True, 'data': out_data}
        )