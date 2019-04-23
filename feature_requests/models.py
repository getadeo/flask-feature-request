from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FeatureRequest(db.Model):

    __tablename__ = 'feature_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'),
        nullable=False)
    client = db.relationship('Client',
        backref=db.backref('feature_requests', lazy=True))

    product_area_id = db.Column(db.Integer, db.ForeignKey('product_areas.id'),
        nullable=False)
    product_area = db.relationship('ProductArea',
        backref=db.backref('feature_requests', lazy=True))
        

class Client(db.Model):

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Client {self.name}>"

    def __str__(self):
        return self.name

class ProductArea(db.Model):

    __tablename__ = 'product_areas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<ProductArea {self.name}>"

    def __str__(self):
        return self.name

