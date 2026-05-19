from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .config import Config

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)

    from .routes.auth import auth_bp
    from .routes.posts import posts_bp
    from .routes.comments import comments_bp
    from .routes.interactions import interaction_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp, url_prefix="/feed")
    app.register_blueprint(comments_bp, url_prefix="/comments")
    app.register_blueprint(interaction_bp)
   
    return app