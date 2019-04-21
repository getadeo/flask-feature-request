from feature_requests import api, web, config
from feature_requests.models import db

from flask import Flask
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello'

    app.register_blueprint(api.bp)
    app.register_blueprint(web.bp)

    app.config.from_object(config)

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
