from flask import Flask, session
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models.models import db, User
from app.translations import t as translate

login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Make t() available in all templates
    @app.context_processor
    def inject_globals():
        lang = session.get('lang', 'en')
        return dict(
            lang=lang,
            t=lambda key: translate(key, lang)
        )

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.villas import villas_bp
    from app.routes.services import services_bp
    from app.routes.admin import admin_bp
    from app.routes.b2b import b2b_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(villas_bp, url_prefix='/villas')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(b2b_bp, url_prefix='/b2b')

    return app
