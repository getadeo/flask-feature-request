import unittest

import requests
from flask_testing import TestCase

from feature_requests import create_app, db, config
from feature_requests.models import Client, ProductArea


app = create_app()

# Fixture Data
clients = ['Client A', 'Client B', 'Client C']
product_areas = ['Policies', 'Billing', 'Claims', 'Reports']

class FeatureRequestTestModels(TestCase):

    def create_app(self):

        app.config.from_object(config.TestingConfig)
        return app

    def setUp(self):

        # Create Database
        db.create_all()

        # Database seeding
        for client in clients:
            c = Client(client)
            db.session.add(c)

        for product_area in product_areas:
            pa = ProductArea(product_area)
            db.session.add(pa)

        db.session.commit()
        # Endof Database Seeding

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def test_client_fixtures(self):

        c = Client.query.all()

        self.assertEqual(
            str(c),
            "[<Client Client A>, <Client Client B>, <Client Client C>]",
            f"Should Return {clients}"
        )

    def test_client_fixtures(self):

        c = ProductArea.query.all()

        self.assertEqual(
            str(c),
            "[<ProductArea Policies>, <ProductArea Billing>," \
                " <ProductArea Claims>, <ProductArea Reports>]",
            f"Should Return data {product_areas}"
        )


if __name__ == '__main__':
    unittest.main()