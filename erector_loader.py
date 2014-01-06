"""
Wrapper for loading Erector template objects.
"""

from django.conf import settings
from django.template.loader import BaseLoader
from django.template.base import TemplateDoesNotExist
from django.utils._os import safe_join
from django.utils.importlib import import_module

import sys, os

class Loader(BaseLoader):
  """
  Loads Erector template objects so they may be correctly rendered with a
  context.
  """

  is_usable = True

  def __init__(self, *args, **kwargs):
    super(Loader, self).__init__(*args, **kwargs)
    self.loaded = {}

  def get_template_sources(self, template_name, template_dirs=None):
    """
    Returns the absolute paths to "template_name", when appended to each
    directory in "template_dirs". Any paths that don't lie inside one of the
    template dirs are excluded from the result set, for security reasons.

    Code taken from django.template.loaders.filesystem.Loader
    """
    if not template_dirs:
      template_dirs = settings.TEMPLATE_DIRS
    for template_dir in template_dirs:
      try:
        yield safe_join(template_dir, template_name)
      except UnicodeDecodeError:
        # The template dir name was a bytestring that wasn't valid UTF-8.
        raise
      except ValueError:
        # The joined path was located outside of this particular
        # template_dir (it might be inside another one, so this isn't
        # fatal).
        pass

  def load_template(self, template_name, template_dirs=None):
    if template_name in self.loaded:
      return self.loaded[template_name]
    tried = []
    for filepath in self.get_template_sources(template_name, template_dirs):
      try:
        dirname, filename = os.path.split(filepath)
        if dirname not in sys.path:
          sys.path.insert(0, dirname)
        print >> sys.stderr, "Trying to import", filename
        template_file = __import__(filename)
        print >> sys.stderr, "Import successful"
      except ImportError as e:
        print >> sys.stderr, "Import failed"
        print >> sys.stderr, e
        tried.append(filepath)
        continue
      try:
        # Return the class so it may be instantiated with a context
        template = getattr(template_file, template_name)
        self.loaded[template_name] = template
        return template, None
      except AttributeError:
        print >> sys.stderr, "Attribute access failed"
        tried.append(filepath)
    if tried:
      error_msg = "Tried %s" % tried
    else:
      error_msg = "Your TEMPLATE_DIRS is empty. Change it to point to at least one template directory."
    raise TemplateDoesNotExist(error_msg)
