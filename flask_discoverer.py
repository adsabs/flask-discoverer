from flask import current_app, Response
import json

DEFAULT_CONFIG = {
  'DISCOVERER_PUBLISH_ENDPOINT':'/resources',
  'DISCOVERER_SELF_PUBLISH':False,
}

class Discoverer(object):
  '''
  API endpoint autodiscovery
  '''

  def __init__(self, app=None, **kwargs):
    self.app = app
    self.kwargs = kwargs if kwargs else {}
    if app is not None:
      self.init_app(app)

  def init_app(self, app, **kwargs):
    self.app = app
    self.kwargs.update(kwargs)
    if not hasattr(app, 'extensions'):
      app.extensions = {}
    if 'discoverer' in app.extensions:
      raise RuntimeError("Flask application already initialized")
    app.extensions['discoverer'] = self
    config = app.config

    for k,v in DEFAULT_CONFIG.iteritems():
      config.setdefault(k,v)
      if k in self.kwargs:
        config.update({k:self.kwargs[k]})

    route = config['DISCOVERER_PUBLISH_ENDPOINT']
    with self.app.app_context():
      current_app.add_url_rule(route,route,lambda: self.find_resources(config['DISCOVERER_SELF_PUBLISH']))

  def find_resources(self,self_publish=False):
    resources = {}
    for rule in current_app.url_map.iter_rules():
      if not self_publish and rule.rule == current_app.config['DISCOVERER_PUBLISH_ENDPOINT']:
        continue
      resources[rule.rule] = {}
      f = current_app.view_functions[rule.endpoint]
      advertised = f._advertised if hasattr(f,'_advertised') else []
      resources[rule.rule].update(description=f.__doc__)
      resources[rule.rule].update(methods=list(rule.methods))
      for key in advertised:
        if hasattr(f,'view_class'):
          resources[rule.rule].update({key:f.view_class.__getattribute__(f.view_class,key)})
        if hasattr(f,key):
          resources[rule.rule].update({key:f.__getattribute__(key)})
    return Response(json.dumps(resources), mimetype='application/json')

def advertise(*args,**kwargs):
  def decorator(f):
    #Set the function attribute
    for key,value in kwargs.iteritems():
      f.__setattr__(key,value)
    #Keep track of which attributes need to be advertised
    for key in kwargs.keys()+list(args):
      if not hasattr(f,'_advertised'):
        f._advertised = []
      f._advertised.append(key)
    return f
  return decorator

