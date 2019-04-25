from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FeatureRequest(db.Model):

    __tablename__ = 'feature_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.Integer)
    target_date = db.Column(db.DateTime)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'),
        nullable=False)
    client = db.relationship('Client',
        backref=db.backref('feature_requests', lazy=True))

    product_area_id = db.Column(db.Integer, db.ForeignKey('product_areas.id'),
        nullable=False)
    product_area = db.relationship('ProductArea',
        backref=db.backref('feature_requests', lazy=True))

    @classmethod
    def save(cls, **data):

        # * Query Existing Feature Request
        fr_exist = cls.query
        fr_exist = fr_exist.filter_by(
            priority=data['priority'],
            client_id=data['client_id']
        ).first()

        # * Increments the priority if Feature Request exist
        # TODO: Look for faster approach
        while fr_exist:
            fr_exist.priority += 1
            db.session.add(fr_exist)
            db.session.commit()

            # * Assign Feature Request if still exist
            fr_exist = cls.query
            fr_exist = fr_exist.filter_by(
                priority=data['priority'],
                client_id=data['client_id']
            ).first()

        # * Insert current Feature Request
        fr = cls(**data)
        db.session.add(fr)
        db.session.commit()

        return fr

    @classmethod
    def edit(cls, **data):

        fr_id_to_update = data.pop('id')

        # * Query Feature to be updated
        fr = cls.query.filter_by(id=fr_id_to_update).first()

        # * Query other existing feature request
        fr_exist = cls.query
        fr_exist = fr_exist.filter_by(
            priority=data['priority'],
            client_id=data['client_id']
        ).first()

        # * Increments the priority if other feature request exist
        # TODO: Look for faster approach
        while fr_exist:
            fr_exist.priority += 1
            db.session.add(fr_exist)
            db.session.commit()

            # * Assign Feature Request if still exist
            fr_exist = cls.query
            fr_exist = fr_exist.filter_by(
                priority=data['priority'],
                client_id=data['client_id']
            ).first()

        # * Update current Feature Request
        for key, value in data.items():
            setattr(fr, key, value)
        db.session.commit()

        return fr

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

