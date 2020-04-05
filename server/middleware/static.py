from flask import send_from_directory


def static_routes(app):
    @app.route('/js/<path:path>', methods=['GET'])
    def send_js(path):
        return send_from_directory('client/static/js', path)

    @app.route('/css/<path:path>', methods=['GET'])
    def send_css(path):
        return send_from_directory('client/static/css', path)

    @app.route('/assets/<path:path>', methods=['GET'])
    def send_asset(path):
        return send_from_directory('client/static/assets', path)

    @app.route('/alb-js/<path:path>', methods=['GET'])
    def send_alb_js(path):
        return send_from_directory('client/static/albinsonium/alb-js', path)

    @app.route('/alb-css/<path:path>', methods=['GET'])
    def send_alb_css(path):
        return send_from_directory('client/static/albinsonium/alb-css', path)
