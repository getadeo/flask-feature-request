import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    TESTING = False
class DevelopmentConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'sqlite:///' + os.path.join(BASE_DIR, 'db/app.db'))
    DEBUG = True

class TestingConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db/test.db')
    TESTING = True
