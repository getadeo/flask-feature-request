import os

from feature_requests import config
from feature_requests.models import db
from feature_requests.routes import api, web

from flask import Flask
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello'

    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(web.bp, url_prefix='/app')

    FLASK_ENV = os.getenv('FLASK_ENV')
    if FLASK_ENV == "development":
        app.config.from_object(config.DevelopmentConfig)

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
