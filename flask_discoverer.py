from flask import current_app

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

class Discoverer(object):
  def __init__(self, app=None):
    self.app = app
    if app is not None:
      self.init_app(app)

  def init_app(self, app):
    raise NotImplementedError
