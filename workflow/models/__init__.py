from process import Process
from step import Step
from work import Work
from work import WorkHistory
from dynamicfield import DynamicFieldStep, DynamicFieldProcess, WorkFieldValue, ProcessFieldValue
from attachment import Attachment
from userprofile import UserProfile

from client.models import Client

from django.contrib import databrowse
databrowse.site.register(Process)
databrowse.site.register(Step)
databrowse.site.register(Work)
databrowse.site.register(Client)


#__all__ = ['Process','Step']
'''
import os
import re
import types
import unittest

PACKAGE = 'workflow.models'
MODEL_RE = r"^.*.py$"

# Search through every file inside this package.
model_names = []
model_dir = os.path.dirname( __file__)
for filename in os.listdir(model_dir):
  if not re.match(MODEL_RE, filename) or filename == "__init__.py":
    continue
  # Import the model file and find all clases inside it.
  model_module = __import__('%s.%s' % (PACKAGE, filename[:-3]),
                           {}, {},
                           filename[:-3])
  for name in dir(model_module):
    item = getattr(model_module, name)
    if not isinstance(item, (type, types.ClassType)):
      continue
    # Found a model, bring into the module namespace.
    exec "%s = item" % name
    model_names.append(name)

# Hide everything other than the classes from other modules.
__all__ = model_names
'''
