
import types

from base_widget import Widget
from buffer import Buffer

from requirements import WidgetRequirementsMixin
from static_content import WidgetCacheMixin

from html_tag import HtmlTag
import html

class HtmlWidget(Widget, WidgetCacheMixin, WidgetRequirementsMixin):

  def __init__(self, context):
    super(HtmlWidget, self).__init__(context)

  """
  def __getattr__(self, tag_name):
    try:
      properties = html.valid_html[tag_name]
    except KeyError:
      return super(HtmlWidget, self).__getattr__(tag_name)
    else:
      def pass_buffer(**kwargs):
        return HtmlTag(self.buffer, tag_name, **kwargs)
      setattr(self, tag_name, pass_buffer)
      return pass_buffer
  """

  def _render(self):
    self.buffer = Buffer()
    self.html().wrap(self.content)
    return "\n".join(self.buffer)

# Monkey-patch HtmlWidget to have all the HTML tag methods
def make_tag_func(name):
  def f(self, **kwargs):
    return HtmlTag(self.buffer, name, **kwargs)
  return f
for name in html.valid_html:
  f = make_tag_func(name)
  setattr(HtmlWidget, name, types.MethodType(f, None, HtmlWidget))
