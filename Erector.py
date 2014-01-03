
import sys

from django.template.loader import BaseLoader
from django.template.base import Template, TemplateDoesNotExist, VariableDoesNotExist

from element import *
from html_tag import *
import html
from static_content import *
from requirements import *
from externals import *

class BadReturnType(Exception): pass

def html_inline(method_or_generator):
  if isinstance(method_or_generator, Generator):
    g = method_or_generator
  elif hasattr(method_or_generator, '__call__'):
    m = method_or_generator
    g = m()
    if not isinstance(method_or_generator, Generator):
      raise BadReturnType("%s() should return a Generator" % (m.__name__,))
  return HtmlTag.render(g)

class Widget(Template, WidgetCacheMixin, WidgetRequirementsMixin):
  """
  Base class for Erector template objects. Implement the content() method to
  yield the desired content.
  """

  required = []

  @classmethod
  def requirements(self):
    return set([r for klass in self.__mro__ if issubclass(klass , Widget) for r in klass.required])

  def __init__(self, context):
    self.verify_requirements(context)
    self._context = context

  def __getattr__(self, method):
    """
    Return a method that passes this instance's buffer as the first argument in
    addition to other arguments.

    Used for elegant buffer sharing with helper methods.
    """
    try:
      properties = html.valid_html[method]
    except:
      raise
    else:
      def pass_buffer(**kwargs):
        HtmlTag(self.buffer, method, **kwargs)()
      setattr(self, method, pass_buffer)
      return pass_buffer

  def v(self, attr):
    """
    Return the context variable of the given name.
    """
    try:
      return self._context[attr]
    except:
      raise

  def content(self):
    """
    Implement this method to yield the desired content.

    The content of this method will automatically be wrapped in <html> tags.
    """
    raise NotImplementedError

  @HtmlTag("html")
  def _wrapped_content(self):
    # Explicit extraction to reduce generator depth
    return self.content()

  def _render(self):
    """
    Return the string with the rendered version of this Widget with the context.
    """

    self.buffer = Buffer()
    return HtmlTag.render(self._wrapped_content())

  def to_tag(self):
    """
    Return this widget as a HtmlTag so it may be rendered in the context of another
    widget. Analagous to partials.
    """
    return self._wrapped_content()

  @classmethod
  def render(klass, context):
    """
    Will be called by clients that load this template with the Erector loader.
    """
    return klass(context)._render()
