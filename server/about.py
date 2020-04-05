from client.TemplateManager.TemplateManager import template_manager


def about_routes(app):
    @app.route("/about", methods=['GET'])
    def about_route():
        return template_manager.get_template('about.html')