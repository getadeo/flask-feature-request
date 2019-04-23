import unittest

from flask_script import Manager

from feature_requests import create_app
from feature_requests.models import ProductArea, Client, db

app = create_app()

manager = Manager(app)

@manager.command
def seed():
    clients = ['Client A', 'Client B', 'Client C']
    product_areas = ['Policies', 'Billing', 'Claims', 'Reports']

    for client in clients:
        c = Client(client)
        db.session.add(c)

    for product_area in product_areas:
        pa = ProductArea(product_area)
        db.session.add(pa)

    db.session.commit()

    return 'Database seeded'


@manager.command
def test():
    tests = unittest.TestLoader().discover('tests', pattern='*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == "__main__":
    manager.run()