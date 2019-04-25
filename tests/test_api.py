import unittest
import json

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

    def test_api_root_endpoint_successful(self):

        r = requests.get(self.get_server_url() + "/api")

        self.assertEqual(
            r.status_code,
            200,
            "Root API Endpoint Should Response 200 Status Code"
        )

    def test_api_feature_request_post(self):

        endpoint = self.get_server_url() + "/api/feature_requests"

        payload = {
            "title": "Test Title 1",
            "description": "Test Description 1",
            "priority": 1,
            "client_id": 1,
            "target_date": "2019-04-28",
            "product_area_id": 1

        }

        r = requests.post(endpoint, json=payload)

        response_data = r.json()

        self.assertEqual(
            r.status_code,
            201,
            "Post request should return 201"
        )

        self.assertEqual(
            response_data['message'],
            "created",
            "JSON reponse message should be 'created'"
        )

        self.assertEqual(
            'featureRequestData' in response_data,
            True,
            "featureRequestData Object should be present"
        )

        self.assertEqual(
            'id' in response_data['featureRequestData'],
            True,
            "JSON response id should be present"
        )

    def test_api_feature_requests_get(self):

        endpoint = self.get_server_url() + "/api/feature_requests"

        first_payload = {
            "title": "Test Title 1",
            "description": "Test Description 1",
            "priority": 1,
            "client_id": 1,
            "target_date": "2019-04-28",
            "product_area_id": 1

        }

        r = requests.post(endpoint, json=first_payload)

        response_data = r.json()

        second_payload = {
            "title": "Test Title 1",
            "description": "Test Description 1",
            "priority": 1,
            "client_id": 1,
            "target_date": "2019-04-28",
            "product_area_id": 1

        }

        r2 = requests.post(endpoint, json=second_payload)

        response_data = r2.json()

        get_frs = requests.get(endpoint)
        frs = get_frs.json()

        self.assertEqual(
            'featureRequests' in frs,
            True,
            "featureRequests JSON object should be present"
        )

        self.assertEqual(
            len(frs['featureRequests']),
            2,
            "featureRequests JSON object length must be 2"
        )

        self.assertEqual(
            get_frs.status_code,
            200,
            "featureRequests request should return 200"
        )

    def test_api_feature_requests_get_via_id(self):

        endpoint = self.get_server_url() + "/api/feature_requests"

        payload = {
            "title": "Test Title 1",
            "description": "Test Description 1",
            "priority": 1,
            "client_id": 1,
            "target_date": "2019-04-28",
            "product_area_id": 1

        }

        r = requests.post(endpoint, json=payload)

        response_data = r.json()['featureRequestData']

        get_fr = requests.get(endpoint + "/" + str(response_data['id']))

        fr_data = get_fr.json()

        self.assertEqual(
            get_fr.status_code,
            200,
            "Feature Request via ID should return 200"
        )

        self.assertEqual(
            fr_data['featureRequestData']['title'],
            payload['title'],
            "Feature Request response title should" \
                " be equal to fixture title payload"
        )

    def test_api_feature_requests_get_via_id_not_found(self):

            endpoint = self.get_server_url() + "/api/feature_requests"

            get_fr = requests.get(endpoint + "/100")

            fr_data = get_fr.json()

            self.assertEqual(
                get_fr.status_code,
                404,
                "Feature Request via ID should return 404"
            )

            self.assertEqual(
                fr_data['message'],
                "Feature Request not found",
                "Error message should be 'Feature Request not found'"
            )

    def test_api_feature_requests_patch_via_id(self):

        endpoint = self.get_server_url() + "/api/feature_requests"

        existing_payload = {
            "title": "Test Title 1",
            "description": "Test Description 1",
            "priority": 1,
            "client_id": 1,
            "target_date": "2019-04-28",
            "product_area_id": 1

        }

        r = requests.post(endpoint, json=existing_payload)

        update_payload = {
            "title": "Updated Test Title 1",
            "description": "Updated Test Description 1",
            "priority": 2,
            "client_id": 3,
            "target_date": "2019-04-28",
            "product_area_id": 1
        }

        response_data = r.json()['featureRequestData']

        r2 = requests.patch(
            endpoint + "/" + str(response_data['id']),
            json=update_payload
        )

        updated_response_data = r2.json()['featureRequestData']

        self.assertEqual(
            updated_response_data['title'],
            update_payload['title'],
            f"Updated feature request should be equal to " \
                " '{update_payload['title']}'"
        )

        self.assertEqual(
            r2.status_code,
            200,
            "Update feature request should return 200"
        )

    def test_api_feature_requests_patch_via_id_not_found(self):

        endpoint = self.get_server_url() + "/api/feature_requests"

        payload = {
            "title": "Test Title 1",
            "description": "Test Description 1",
            "priority": 1,
            "client_id": 1,
            "target_date": "2019-04-28",
            "product_area_id": 1

        }

        r = requests.patch(endpoint + "/100", json=payload)

        self.assertEqual(
            r.status_code,
            404,
            "Feature Request via ID should return 404"
        )

        self.assertEqual(
            r.json()['message'],
            "Feature Request not found",
            "Error message should be 'Feature Request not found'"
        )


if __name__ == '__main__':
    unittest.main()