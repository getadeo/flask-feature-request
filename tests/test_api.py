import unittest

import requests
from flask_testing import LiveServerTestCase

from feature_requests import create_app, db, config
from feature_requests.models import Client, ProductArea


app = create_app()

class FeatureRequestTestAPI(LiveServerTestCase):

    def create_app(self):

        app.config.from_object(config.TestingConfig)
        return app

    def setUp(self):

        db.create_all()

        clients = ['Client A', 'Client B', 'Client C']
        product_areas = ['Policies', 'Billing', 'Claims', 'Reports']
        
        for client in clients:
            c = Client(client)
            db.session.add(c)

        for product_area in product_areas:
            pa = ProductArea(product_area)
            db.session.add(pa)

        db.session.commit()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def test_api_root_endpoint(self):

        r = requests.get(self.get_server_url() + "/api")

        self.assertEqual(r.status_code, 200, "Root API Endpoint Should Response 200 Status Code")


if __name__ == '__main__':
    unittest.main()