def init_app(app):
    from src.routes.authRoutes import auth_bp
    from .mainRoutes import main_bp
    from .userRoutes import user_bp
    from .projectRoutes import project_bp
    from .machineRoutes import machine_bp
    from .solventRoutes import solvent_bp
    from .samplePreparationRoutes import sample_preparation_bp
    from .sampleRoutes import sample_bp
    from .homeRoutes import home_bp
    from .solicitudesRoutes import solicitudes_bp
    from .nucleoRoutes import nucleo_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(machine_bp)
    app.register_blueprint(solvent_bp)
    app.register_blueprint(sample_preparation_bp)
    app.register_blueprint(sample_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(solicitudes_bp)
    app.register_blueprint(nucleo_bp)
