from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    return app