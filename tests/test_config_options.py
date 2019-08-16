from flask import Flask
from flask_testing import TestCase
# from flask.ext.testing import TestCase
import unittest

try:
    from flask_discoverer import Discoverer, advertise
except ImportError:
    import sys
    sys.path.append('..')
    from flask_discoverer import Discoverer, advertise

    
class TestConfigOptions(TestCase):
    def create_app(self):
        app = Flask(__name__, static_folder=None)
        
        @app.route('/foo')
        @advertise(thisattr='bar')
        def foo():
            '''foo docstring'''
            return "foo route"
        return app

    def test_resource_publish_endpoint1(self):
        discoverer = Discoverer(self.app, DISCOVERER_PUBLISH_ENDPOINT='/non-default-resources')
        self.assertEqual(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'], '/non-default-resources')
        r = self.client.get('/resources')
        self.assertStatus(r, 404)
        r = self.client.get('/non-default-resources')
        self.assertStatus(r, 200)
        self.assertIn('/foo', r.json)

    def test_resource_publish_endpoint2(self):
        discoverer = Discoverer()
        discoverer.init_app(self.app, DISCOVERER_PUBLISH_ENDPOINT='/non-default-resources2')
        self.assertEqual(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'], '/non-default-resources2')
        r = self.client.get('/resources')
        self.assertStatus(r, 404)
        r = self.client.get('/non-default-resources2')
        self.assertStatus(r, 200)
        self.assertIn('/foo', r.json)  

    def test_selfpublish_true(self):
        discoverer = Discoverer(self.app, DISCOVERER_SELF_PUBLISH=True)
        r = self.client.get(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'])
        self.assertStatus(r, 200)
        self.assertIn(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'], r.json)

    def test_selfpublish_false(self):
        discoverer = Discoverer(self.app, DISCOVERER_SELF_PUBLISH=False)
        r = self.client.get(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'])
        self.assertStatus(r, 200)
        self.assertNotIn(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'], r.json)


if __name__ == '__main__':
    unittest.main(verbosity=2)
