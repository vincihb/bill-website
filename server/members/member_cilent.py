from client.TemplateManager.TemplateManager import template_manager


def member_client_routes(app):
    @app.route("/members", methods=['GET'])
    def get_members():
        return template_manager.get_template('member.html')

    @app.route("/member", methods=['GET'])
    def get_member_null_id():
        return template_manager.get_template('member_not_found.html')

    @app.route("/member/", methods=['GET'])
    def get_member_null_id_slash():
        return template_manager.get_template('member_not_found.html')

    @app.route("/member/<string:member_id>", methods=['GET'])
    def get_member(member_id):
        print(member_id)
        return template_manager.get_template('member.html')
