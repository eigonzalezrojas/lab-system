from flask import Blueprint


def init_app(app):
    from .authRoutes import auth_bp
    from .mainRoutes import main_bp
    from .userRoutes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
