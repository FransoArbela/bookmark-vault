from .health import bp as health_bp
from .auth import bp as auth_bp
from .bookmarks import bp as bookmarks_bp

def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bookmarks_bp)
