[![Build Status](https://travis-ci.org/adsabs/flask-discoverer.svg?branch=master)](https://travis-ci.org/adsabs/flask-discoverer)

# Flask discoverer

Flask extension that supports the introspection of resources and resource attributes such as ratelimits or permissions. After initializing, these attributes will be published as JSON via a `/resources` endpoint.

## Initialization
    from flask import Flask
    from flask_discoverer import Discoverer

    app = Flask(__name__)
    discoverer = Discoverer(app)

or, alternatively:

    app = Flask(__name__)
    discoverer = Discoverer()
    discoverer.init_app(app)
    
## Usage

TBD
