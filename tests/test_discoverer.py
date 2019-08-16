from flask import Flask
from flask_testing import TestCase
from flask.views import MethodView
import unittest

try:
    from flask_discoverer import Discoverer, advertise
except ImportError:
    import sys
    sys.path.append('..')
    from flask_discoverer import Discoverer, advertise


def compare_dicts(s, a, b):
    """python 2 and 3 compatible code that works with test data"""
    s.assertEqual(a['/scoped']['scopes'], b['/scoped']['scopes'])
    s.assertEqual(a['/scoped']['description'], b['/scoped']['description'])
    s.assertEqual(sorted(a['/scoped']['methods']), sorted(b['/scoped']['methods']))
    s.assertEqual(a['/default']['description'], b['/default']['description'])
    s.assertEqual(sorted(a['/default']['methods']), sorted(b['/default']['methods']))

    
class TestFlaskRestfulBasedApp(TestCase):
    def create_app(self):
        from flask_restful import Resource, Api 
        app = Flask(__name__, static_folder=None)
        
        class DefaultView(Resource):
            '''Default route docstring'''
            def put(self):
                return "put on default route"
            
            def post(self):
                return "post on default route"
        
        class ScopedView(Resource):
            '''Scoped route docstring'''
            scopes = ['default']
            decorators = [advertise('scopes')]
            
            def get(self):
                return "scoped route"
        
        self.expected_resources = {
            '/scoped': {
                'scopes': ['default'],
                'description': 'Scoped route docstring',
                'methods': ['HEAD', 'OPTIONS', 'GET'],
            },
            '/default': {
                'description': 'Default route docstring',
                'methods': ['PUT', 'POST', 'OPTIONS'],
            },
        }

        api = Api(app)
        api.add_resource(DefaultView, '/default')
        api.add_resource(ScopedView, '/scoped')
        discoverer = Discoverer(app)
        return app

    def test_restful_routes(self):
        '''
        Test that discoverer plays nicely with flask-restful in the sense
        that restful routes work as expected
        '''
        r = self.client.get('/scoped')
        self.assertStatus(r, 200)
        r = self.client.post('/default')
        self.assertStatus(r, 200)
        r = self.client.get('/default')
        self.assertStatus(r, 405)

    def test_resources(self):
        r = self.client.get(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'])
        compare_dicts(self, r.json, self.expected_resources)


class TestFunctionBasedViewsApp(TestCase):
    '''
    Test discoverer against an application created 
    using Flask's function based views pattern (i.e. @app.route)
    '''
    def create_app(self):
        app = Flask(__name__, static_folder=None)
        
        @app.route('/default', methods=['POST', 'PUT'])
        def default():
            '''Default route docstring'''
            return "default route"

        @advertise(scopes=['default'])
        @app.route('/scoped')
        def scoped():
            '''Scoped route docstring'''
            return "scoped route"

        self.expected_resources = {
            '/scoped': {
                'scopes': ['default'],
                'description': 'Scoped route docstring',
                'methods': ['HEAD', 'OPTIONS', 'GET'],
            },
            '/default': {
                'description': 'Default route docstring',
                'methods': ['PUT', 'POST', 'OPTIONS'],
            },
        }
        discoverer = Discoverer(app)
        return app

    def test_resources(self):
        r = self.client.get(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'])
        compare_dicts(self, r.json, self.expected_resources)


class TestClassBasedViewsApp(TestCase):
    '''
    Test discoverer against an application created 
    using class based based views pattern (i.e. @app.route)
    '''
    def create_app(self):
        
        class DefaultView(MethodView):
            '''Default route docstring'''
            def put(self):
                return "put on default route"
            
            def post(self):
                return "post on default route"
        
        class ScopedView(MethodView):
            '''Scoped route docstring'''
            scopes = ['default']
            decorators = [advertise('scopes')]
            
            def get(self):
                return "scoped route"

        app = Flask(__name__, static_folder=None)
        app.add_url_rule('/default', view_func=DefaultView.as_view('default'))
        app.add_url_rule('/scoped', view_func=ScopedView.as_view('scoped'))
        discoverer = Discoverer(app)

        self.expected_resources = {
            '/scoped': {
                'scopes': ['default'],
                'description': 'Scoped route docstring',
                'methods': ['HEAD', 'OPTIONS', 'GET'],
            },
            '/default': {
                'description': 'Default route docstring',
                'methods': ['PUT', 'POST', 'OPTIONS'],
            },
        }
        return app

    def test_resources(self):
        r = self.client.get(self.app.config['DISCOVERER_PUBLISH_ENDPOINT'])
        compare_dicts(self, r.json, self.expected_resources)


if __name__ == '__main__':
    unittest.main(verbosity=2)
