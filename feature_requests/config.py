import os

SQLALCHEMY_DATABASE_URI = os.getenv(
  'SQLALCHEMY_DATABASE_URI',
  'sqlite:///tmp/app.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False

