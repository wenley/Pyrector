
import cgi
from types import GeneratorType as Generator
from element import Element

def make_html_safe(s):
  if s.html_safe:
    return s
  else:
    s = cgi.escape(str(s))
    s.html_safe = True
    return s
def html_safe(s):
  s.html_safe = True
  return s

# Is this necessary?
def escape_quote(s,force=False):
  if s.quote_escape:
    return s
  else:
    s = s.replace('"', r"\"").replace("'", r"\'")
    s.quote_escape = True
    return s

class InvalidHtmlTagUse(Exception): pass

# Consider HTML escaping?
class HtmlTag(Element):
  """An HTML tag. See __init__ docstring for details on use."""

  def __init__(self, buffer, tag_name, class_=None, text="", **kwargs):
    """
    Create an HTML tag for Widget rendering.

    When created as a piece of content to be yielded, it may take text as a
    keyword argument.

    When created as a decorator for a method that yields content, it nests the
    content in a tag of its type.

    Arguments:
    tag_name -- The type of HTML tag (e.g. head, body, p)

    Keyword Arguments:
    class_ -- The CSS class of the tag
    text   -- Text to be put in the body of the tag. It will be HTML escaped.
              Incompatible with decorator syntax for nested tags.

    Other keyword arguments will be interpreted as HTML tag attributes.

    Example:
    >>> t = HtmlTag("p", "This is a <p> tag with &lt;p&gt; afterwards")
    >>> HtmlTag.render(t)
    <p>This is a &lt;p&gt; tag with &amp;lt;p&amp;gt; afterwards</p>

    >>> @HtmlTag("p", class_="red", attribute_name="attribute_val")
    ... def some_content():
    ...   yield "content"
    >>> HtmlTag.render(some_content())
    <p class="red" attribute_name="attribute_val">content</p>
    """

    self.buffer = buffer
    self.tag_name = tag_name
    self.inner_text = text
    self.fields = kwargs
    if class_ is not None:
      self.fields['class'] = class_

  # Used for decorator syntax for tags with children
  def __call__(self, method=None):
    if not method:
      self.emit_open()
      self.emit_inside()
      self.emit_close()
    else:
      if self.inner_text:
        raise InvalidHtmlTagUse("Body text cannot be specified for a decorator HtmlTag")
      def wrapper(*args):
        self.emit_open()
        method(*args)
        self.emit_close()
      wrapper.orig = method
      return wrapper

  # Wraps own formatting around some text
  def text(self, text):
    if self.inner_text:
      print >> sys.stderr, "Inner text is", self.inner_text
      raise InvalidHtmlTagUse("Cannot wrap formatting with existing text around new text")
    self.inner_text = text
    self()
    self.inner_text = None
  def wrap(self, method):
    self(method)()

  # Push content to the buffer
  def emit_open(self):
    self.buffer.append(self._open_tag())
  def emit_inside(self):
    if self.inner_text:
      self.buffer.append(self.inner_text)
  def emit_close(self):
    self.buffer.append(self._close_tag())

  # Constructs the opening HTML tag for this TAG
  # @return String
  def _open_tag(self):
    '''Creates the opening tag for this element'''
    s = "<%s " % (self.tag_name,)
    s += " ".join('%s="%s"' % (str(key), str(val)) for key, val in self.fields.iteritems())
    s += ">"
    return s

  # Constructs the closing HTML tag for this HtmlTag
  # @return String
  def _close_tag(self):
    '''Returns the closing tag for this element'''
    return "</%s>" % (self.tag_name,)

