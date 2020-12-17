[![Build Status](https://travis-ci.org/adsabs/flask-discoverer.svg?branch=master)](https://travis-ci.org/adsabs/flask-discoverer)

# Flask discoverer

 Flask-discoverer is a Flask extension that supports the introspection of resources and resource attributes such as ratelimits or permissions. After initializing, these attributes will be published as JSON via a `/resources` endpoint.
 
## Installation

    pip install flask-discoverer
    
or, alternatively:

    git clone https://github.com/adsabs/flask-discoverer
    cd flask-discoverer
    ./setup.py install

## Quickstart example

    from flask import Flask
    from flask.ext.discoverer import Discoverer, advertise

    app = Flask(__name__,static_folder=None)
    discoverer = Discoverer(app)

    @app.route('/route1')
    def route1():
      '''docstring for route1'''
      return "route1"

    @advertise(private=True,colors=["red","green"])
    @app.route('/route2')
    def route2():
      '''docstring for route2'''
      return "route2"

    app.run(host='127.0.0.1',port=5000)

The app has a `/resources` route added:

    curl "http://127.0.0.1:5000/resources" | python -mjson.tool
    {
        "/route1": {
            "description": "docstring for route1",
            "methods": ["HEAD","OPTIONS","GET"],
        },
        "/route2": {
            "colors": ["red","green"],
            "description": "docstring for route2",
            "methods": ["HEAD","OPTIONS","GET"],
            "private": true
        }
    }


## Usage

### Initialization

    app = Flask(__name__)
    discoverer = Discoverer(app)
    
or, alternatively:

    app = Flask(__name__)
    discoverer = Discoverer()
    ...
    discoverer.init_app(app)
    
### Configuration

Flask-discoverer accepts two configuration parameters. These parameters can be passed as kwargs to `Discoverer(**kwargs)` or `discoverer.init_app(app,**kwargs)`. Alternatively, they can be set in `app.config`.

      # Define the autodiscovery endpoint
    DISCOVERER_PUBLISH_ENDPOINT = '/resources'
      # Advertise its own route within DISCOVERER_PUBLISH_ENDPOINT
    DISCOVERER_SELF_PUBLISH = False

### Class-based views

Flask-discoverer works with class based views such as `Flask.MethodView`. Use the following pattern:

    class ScopedView(MethodView):
      '''Scoped route docstring'''
      scopes = ['default']
      decorators = [advertise('scopes')]
      def get(self):
        return "scoped route"
    
    app = Flask(__name__,static_folder=None)
    app.add_url_rule('/scoped',view_func=ScopedView.as_view('scoped'))
    discoverer = Discoverer(app)
    
    # GET /resources
    #      '/scoped': {
    #          'scopes':['default'],
    #          'description': 'Scoped route docstring',
    #          'methods': ['HEAD','OPTIONS','GET'],
    #  },
    
## Releasing new version to pypi

When a new release is ready, it should be uploaded to pypi. First, try the test environment:

```
python3 -m venv ./venv
source venv/bin/activate
pip install --upgrade setuptools wheel
rm -rf dist/
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
pip install --upgrade twine
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Verify the [testing pypi repository](https://test.pypi.org/project/flask-discoverer/) and if everything looks good, you can proceed to upload to the [official repository](https://pypi.org/project/flask-discoverer/):

```
twine upload dist/*
```
