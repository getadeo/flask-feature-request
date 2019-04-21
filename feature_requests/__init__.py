from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello'

    from feature_requests import api, web
    app.register_blueprint(api.bp)
    app.register_blueprint(web.bp)

    return app
