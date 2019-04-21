from flask import Flask
from feature_requests import api, web
from feature_requests import models
from feature_requests import config

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello'

    app.register_blueprint(api.bp)
    app.register_blueprint(web.bp)

    app.config.from_object(config)


    models.init_app(app)

    return app
