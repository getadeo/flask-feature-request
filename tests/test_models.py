import unittest

import requests
from flask_testing import TestCase

from feature_requests import create_app, db, config
from feature_requests.models import Client, ProductArea, FeatureRequest


app = create_app()

# Fixture Data
CLIENTS = ['Client A', 'Client B', 'Client C']
PRODUCT_AREAS = ['Policies', 'Billing', 'Claims', 'Reports']

class FeatureRequestTestModels(TestCase):

    def create_app(self):

        app.config.from_object(config.TestingConfig)
        return app

    def setUp(self):

        # Create Database
        db.create_all()

        # Database seeding
        for client in CLIENTS:
            c = Client(client)
            db.session.add(c)

        for product_area in PRODUCT_AREAS:
            pa = ProductArea(product_area)
            db.session.add(pa)

        db.session.commit()
        # Endof Database Seeding

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def test_client_fixtures_successful(self):

        c = Client.query.all()

        self.assertEqual(
            str(c),
            "[<Client Client A>, <Client Client B>, <Client Client C>]",
            f"Should Return data {CLIENTS}"
        )

    def test_product_area_fixtures_successful(self):

        c = ProductArea.query.all()

        self.assertEqual(
            str(c),
            "[<ProductArea Policies>, <ProductArea Billing>," \
                " <ProductArea Claims>, <ProductArea Reports>]",
            f"Should Return data {PRODUCT_AREAS}"
        )

    def test_feature_request_save(self):
        feature_data_1 = {
            "title": "Test 1",
            "description": "Test 1 Description",
            "client_id": 1,
            "priority": 1,
            "product_area_id": 1
        }

        feature_data_2 = {
            "title": "Test 2",
            "description": "Test 2 Description",
            "client_id": 2,
            "priority": 2,
            "product_area_id": 2
        }

        f1 = FeatureRequest.save(**feature_data_1)
        f1 = FeatureRequest.query.filter_by(id=f1.id).first()

        f2 = FeatureRequest.save(**feature_data_2)
        f2 = FeatureRequest.query.filter_by(id=f2.id).first()

        self.assertEqual(
            f1 is not None,
            True,
            "Feature 1 should be created"
        )

        self.assertEqual(
            f1.title,
            "Test 1",
            "Feature 1 title should be 'Test 1'"
        )

        self.assertEqual(
            f2.title,
            "Test 2",
            "Feature 1 title should be 'Test 2'"
        )

        self.assertEqual(
            f2 is not None,
            True,
            "Feature 2 should be created"
        )

        self.assertEqual(
            f1.client.name,
            CLIENTS[0],
            f"Feature 1 client should be '{CLIENTS[0]}'"
        )

        self.assertEqual(
            f2.client.name,
            CLIENTS[1],
            f"Feature 2 client should be '{CLIENTS[1]}'"
        )

        self.assertEqual(
            f1.product_area.name,
            PRODUCT_AREAS[0],
            f"Feature 1 client should be '{PRODUCT_AREAS[0]}'"
        )

        self.assertEqual(
            f2.product_area.name,
            PRODUCT_AREAS[1],
            f"Feature 2 client should be '{PRODUCT_AREAS[1]}'"
        )

    def test_feature_request_with_existing_client_and_priority(self):
        feature_data_1 = {
            "title": "Test 1",
            "description": "Test 1 Description",
            "client_id": 1,
            "priority": 1,
            "product_area_id": 2
        }

        f1 = FeatureRequest.save(**feature_data_1)


        feature_data_2 = {
            "title": "Test 2",
            "description": "Test 2 Description",
            "client_id": 1,
            "priority": 1,
            "product_area_id": 2
        }

        
        f2 = FeatureRequest.save(**feature_data_2)

        self.assertEqual(
            f1.priority,
            2,
            "First Feature Request Priority should be 2"
        )

        self.assertEqual(
            f2.priority,
            1,
            "Second Feature Request Priority should be 1"
        )

    def test_feature_request_with_multiple_existing_client_and_priority(self):
            feature_data_1 = {
                "title": "Test 1",
                "description": "Test 1 Description",
                "client_id": 1,
                "priority": 1,
                "product_area_id": 2
            }

            f1 = FeatureRequest.save(**feature_data_1)


            feature_data_2 = {
                "title": "Test 2",
                "description": "Test 2 Description",
                "client_id": 1,
                "priority": 1,
                "product_area_id": 2
            }

            
            f2 = FeatureRequest.save(**feature_data_2)

            feature_data_3 = {
                "title": "Test 3",
                "description": "Test 3 Description",
                "client_id": 1,
                "priority": 1,
                "product_area_id": 2
            }

            f3 = FeatureRequest.save(**feature_data_3)

            f1 = FeatureRequest.query.filter_by(id=f1.id).first()

            f2 = FeatureRequest.query.filter_by(id=f2.id).first()

            f3 = FeatureRequest.query.filter_by(id=f3.id).first()

            self.assertEqual(
                f1.priority,
                2,
                "First Feature Request Priority should be 2"
            )

            self.assertEqual(
                f2.priority,
                2,
                "Second Feature Request Priority should be 2"
            )

            self.assertEqual(
                f3.priority,
                1,
                "Second Feature Request Priority should be 1"
            )

    def test_feature_request_with_padded_multiple_existing_client_and_priority(self):
            feature_data_1 = {
                "title": "Test 1",
                "description": "Test 1 Description",
                "client_id": 1,
                "priority": 1,
                "product_area_id": 2
            }

            f1 = FeatureRequest.save(**feature_data_1)


            feature_data_2 = {
                "title": "Test 2",
                "description": "Test 2 Description",
                "client_id": 1,
                "priority": 4,
                "product_area_id": 2
            }

            
            f2 = FeatureRequest.save(**feature_data_2)

            feature_data_3 = {
                "title": "Test 3",
                "description": "Test 3 Description",
                "client_id": 1,
                "priority": 1,
                "product_area_id": 2
            }

            
            f3 = FeatureRequest.save(**feature_data_3)

            self.assertEqual(
                f1.priority,
                2,
                "First Feature Request Priority should be 2"
            )

            self.assertEqual(
                f2.priority,
                4,
                "Second Feature Request Priority should be 4"
            )

            self.assertEqual(
                f3.priority,
                1,
                "Second Feature Request Priority should be 1"
            )


    def test_feature_request_update(self):
            feature_data_1 = {
                "title": "Test 1",
                "description": "Test 1 Description",
                "client_id": 1,
                "priority": 1,
                "product_area_id": 2
            }

            f1 = FeatureRequest.save(**feature_data_1)

            updated_feature_data_1 = {
                "id": f1.id,
                "title": "Updated Test 1",
                "description": "Updated Test 1 Description",
                "client_id": 1,
                "priority": 1,
                "product_area_id": 2
            }

            f1 = FeatureRequest.edit(**updated_feature_data_1)

            self.assertEqual(
                f1.title,
                updated_feature_data_1['title'],
                f"Title should be {updated_feature_data_1['title']}"
            )

            self.assertEqual(
                f1.description,
                updated_feature_data_1['description'],
                f"Description should be {updated_feature_data_1['description']}"
            )


    def test_feature_request_update_with_existing_client_and_priority(self):

        existing_feature_data = {
            "title": "Existing Feature",
            "description": "TExisting Feature Description",
            "client_id": 2,
            "priority": 1,
            "product_area_id": 2
        }

        ef = FeatureRequest.save(**existing_feature_data)

        feature_data_1 = {
            "title": "Test 1",
            "description": "Test 1 Description",
            "client_id": 1,
            "priority": 1,
            "product_area_id": 2
        }

        f1 = FeatureRequest.save(**feature_data_1)

        updated_feature_data_1 = {
            "id": f1.id,
            "title": "Updated Test 1",
            "description": "Updated Test 1 Description",
            "client_id": 2,
            "priority": 1,
            "product_area_id": 2
        }


        f1 = FeatureRequest.edit(**updated_feature_data_1)

        ef = FeatureRequest.query.filter_by(id=ef.id).first()

        self.assertEqual(
            ef.priority,
            2,
            "Existing Feature Request priority should be 2"
        )

        self.assertEqual(
            f1.priority,
            1,
            "New Feature Request Priority should be 1"
        )


if __name__ == '__main__':
    unittest.main()