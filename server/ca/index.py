from client.TemplateManager.TemplateManager import template_manager


def all_ca_routes(app):
    @app.route('/ca/', methods=['GET'])
    def canadian_root():
        return template_manager.get_template('index.html')
