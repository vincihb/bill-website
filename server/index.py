from server.ca.index import all_ca_routes
from server.middleware.index import middleware_routes
from server.about import about_routes
from server.filter import filter_routes
from server.missing import missing_routes
from server.result import result_routes
from client.TemplateManager.TemplateManager import template_manager


def all_server_routes(app):
    # nested routes
    all_ca_routes(app)
    middleware_routes(app)

    # top-level routes
    about_routes(app)
    filter_routes(app)
    missing_routes(app)
    result_routes(app)

    @app.route("/", methods=['GET'])
    def index_route():
        return template_manager.get_template('index.html')