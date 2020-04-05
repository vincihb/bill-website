from client.TemplateManager.TemplateManager import template_manager


def filter_routes(app):
    @app.route("/filter", methods=['GET'])
    def filter_route():
        return template_manager.get_template('filter.html')