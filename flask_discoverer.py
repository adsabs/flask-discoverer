from flask import current_app
import json

class Discoverer(object):
  '''
  API endpoint autodiscovery
  '''

  def __init__(self, app=None):
    self.app = app
    if app is not None:
      self.init_app(app)

  def init_app(self, app, find_resources=True):
    self.app = app
    self.resources = {}
    if not hasattr(app, 'extensions'):
      app.extensions = {}
    if 'discoverer' in app.extensions:
      raise RuntimeError("Flask application already initialized")
    app.extensions['discoverer'] = self
    config = app.config
    config.setdefault('DISCOVERER_PUBLISH_ENDPOINT','/resources')
    if find_resources:
      with self.app.app_context():
        self.find_resources()

  def find_resources(self,force=False):
    if self.resources and not force:
      raise RuntimeError("Resources were already discovered. Re-discover with force=True")
    resources = {}
    for rule in current_app.url_map.iter_rules():
      resources[rule.rule] = {}
      f = current_app.view_functions[rule.endpoint]
      if hasattr(f,'view_class'):
        f = f.view_class
      resources[rule.rule].update(description=f.__doc__)
      resources[rule.rule].update(methods=list(rule.methods))
      if hasattr(f,'advertised'):
        for key in f.advertised:
          if hasattr(f,key):
            resources[rule.rule].update({key:f.__getattribute__(key)})
    route = current_app.config['DISCOVERER_PUBLISH_ENDPOINT']
    current_app.add_url_rule(route,route,lambda: json.dumps(resources))

def advertise(*args,**kwargs):
  def decorator(f):
    #Set the function attribute
    for key,value in kwargs.iteritems():
      f.__setattr__(key,value)

    #Keep track of which attributes need to be advertised
    for key in kwargs.keys()+args:
      if not hasattr(f,'advertised'):
        advertised = []
      f.advertised.append(key)
      f.__setattr__('advertised',advertised)
    return f
  return decorator