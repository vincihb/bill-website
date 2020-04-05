from server.middleware.static import static_routes


def middleware_routes(app):
    static_routes(app)
