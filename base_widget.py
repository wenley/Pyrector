
from django.template.base import Template
from buffer import Buffer

class Widget(Template):
  """
  Base class for Erector template objects. Implement the content() method to
  yield the desired content.
  """

  def __init__(self, context):
    self._context = context

  def __getattr__(self, variable):
    """
    Return a method that passes this instance's buffer as the first argument in
    addition to other arguments.

    Used for elegant buffer sharing with helper methods.
    """
    try:
      return self._context[variable]
    except:
      raise KeyError(variable + " is not a variable in the given context")

  def v(self, attr):
    """
    Return the context variable of the given name.
    """
    try:
      return self._context[attr]
    except:
      raise

  def text(self, text):
    self.buffer.append(text)

  def content(self):
    """
    Implement this method to yield the desired content.

    The content of this method will automatically be wrapped in <html> tags.
    """
    raise NotImplementedError

  def _render(self):
    """
    Return the string with the rendered version of this Widget with the context.
    """

    self.buffer = Buffer()
    self.content()
    return "\n".join(self.buffer)

  @classmethod
  def render(klass, context={}):
    """
    Will be called by clients that load this template with the Erector loader.
    """
    return klass(context)._render()

  @classmethod
  def as_partial(klass, parent):
    instance = klass(parent.context)
    instance.buffer = parent.buffer
    instance.content()
    parent.buffer = instance.buffer # TODO: Check gratuity of this

