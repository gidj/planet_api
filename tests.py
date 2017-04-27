import unittest
from flask_testing import TestCase
from flask import current_app
import json

from planet import create_app, db
from planet.models import Asset

good_data = [
    {
        "name": "Sample-Satellite_1",
        "asset_type": "satellite",
        "asset_class": "dove",
    },
    {
        "name": "Sample-Satellite_2",
        "asset_type": "satellite",
        "asset_class": "rapideye",
    },
    {
        "name": "Sample-Antenna_1",
        "asset_type": "antenna",
        "asset_class": "dish",
    },
    {
        "name": "Sample-Antenna_2",
        "asset_type": "antenna",
        "asset_class": "yagi",
    },
]


class BaseTest(TestCase):
    API_ENDPOINT = "http://192.168.33.10/api/v1/"
    ASSETS_ENDPOINT = API_ENDPOINT + 'assets/'

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()
        for datum in good_data:
            asset = Asset(**datum)
            db.session.add(asset)
        db.session.commit()
        self.client = current_app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_api_root_links(self):
        r = self.client.get(self.API_ENDPOINT)
        self.assert200(r)
        self.assertTrue('links' in r.json)
        self.assertTrue('Description' in r.json)

    def test_retrieval_of_known_asset(self):
        name = good_data[0]['name']
        r = self.client.get(self.ASSETS_ENDPOINT+name)
        self.assert200(r)
        self.assertTrue(r.json['name'] == name)

    def test_creating_new_asset(self):
        data = {
            "name": "Sample-Antenna_3",
            "type": "antenna",
            "class": "yagi",
        }
        r = self.client.post(self.ASSETS_ENDPOINT,
            data=json.dumps(data),
            content_type='application/json')
        self.assertStatus(r, 201)
        # Query the api again to make sure it's there
        r1 = self.client.get(self.ASSETS_ENDPOINT+data["name"])
        self.assert200(r1)

    def test_creating_asset_with_name_too_short(self):
        data = {
            "name": "123",
            "type": "antenna",
            "class": "yagi",
        }
        r = self.client.post(self.ASSETS_ENDPOINT,
            data=json.dumps(data),
            content_type='application/json')
        self.assert400(r)
        self.assertTrue('4 and 64' in r.json['error'])

    def test_creating_asset_with_name_too_long(self):
        data = {
            "name": "a"*65,
            "type": "antenna",
            "class": "yagi",
        }
        r = self.client.post(self.ASSETS_ENDPOINT,
            data=json.dumps(data),
            content_type='application/json')
        self.assert400(r)
        self.assertTrue('4 and 64' in r.json['error'])

    def test_creating_asset_with_invalid_name(self):
        invalid_names = ("1234!", "_sample", "-name", "hello?")

        for name in invalid_names:
            data = {
                "name": name,
                "type": "antenna",
                "class": "yagi",
            }
            r = self.client.post(self.ASSETS_ENDPOINT,
                data=json.dumps(data),
                content_type='application/json')
            self.assert400(r)
            self.assertTrue('The name you supplied is invalid' in r.json['error'])

    def test_creating_asset_with_wrong_type(self):
        data = {
            "name": "Sample-Mirror",
            "type": "mirror",
            "class": "yagi",
        }
        r = self.client.post(self.ASSETS_ENDPOINT,
            data=json.dumps(data),
            content_type='application/json')
        self.assert400(r)
        self.assertTrue('asset type' in r.json['error'])

    def test_creating_asset_with_no_type(self):
        data = {
            "name": "Sample-Mirror",
            "class": "yagi",
        }
        r = self.client.post(self.ASSETS_ENDPOINT,
            data=json.dumps(data),
            content_type='application/json')
        self.assert400(r)
        self.assertTrue('asset type' in r.json['error'])

    def test_creating_asset_with_wrong_class(self):
        data = {
            "name": "Sample-Antenna_fail",
            "type": "antenna",
            "class": "rapideye",
        }
        r = self.client.post(self.ASSETS_ENDPOINT,
            data=json.dumps(data),
            content_type='application/json')
        self.assert400(r)
        self.assertTrue('asset class' in r.json['error'])

    def test_creating_asset_with_no_class(self):
        data = {
            "name": "Sample-Antenna_fail",
            "type": "antenna",
        }
        r = self.client.post(self.ASSETS_ENDPOINT,
            data=json.dumps(data),
            content_type='application/json')
        self.assert400(r)
        self.assertTrue('asset class' in r.json['error'])

    def test_fail_on_creating_existing_name(self):
        data = {
            "name": good_data[0]['name'],
            "type": good_data[0]['asset_type'],
            "class": good_data[0]['asset_class'],
        }
        r = self.client.post(self.ASSETS_ENDPOINT,
            data=json.dumps(data),
            content_type='application/json')
        self.assert403(r)
        pass

if __name__ == 'main':
    unittest.main()

