
from html_widget import HtmlWidget as Widget

class InlineWidget(Widget):
  
  def __init__(self):
    pass

  def render(self, context={}):
    self._context = context
    self._render()

def inline(method):
  """
  Given a method, produces a Widget that can be rendered given a context.

  >>>@inline
  ...def custom_content(self):
  ...  self.text("I have my own widget!")
  ...
  >>>custom_content.render()
  "I have my own widget!"
  """

  widget = InlineWidget()
  widget.content = method
  return widget
