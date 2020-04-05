from flask import request


def result_routes(app):
    @app.route("/result", methods=['POST'])
    def get_result_and_send_new_title():
        global m
        data = request.get_json()
        if data['init']:
            return m.get_next()
        else:
            m.set_result(data['res'])
            return m.get_next()