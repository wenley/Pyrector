
import cgi
from types import GeneratorType as Generator
from element import Element

# This could allow double-escaping if two escapes are alternated 
class HtmlSafeString(str): pass
def make_html_safe(s):
  if isinstance(s, HtmlSafeString):
    return s
  elif isinstance(s, str):
    return HtmlSafeString(cgi.escape(s))
  else:
    return HtmlSafeString(cgi.escape(str(s)))
def html_safe(s):
  return HtmlSafeString(s)

# Is this necessary?
class QuoteEscapedString(str): pass
def escape_quote(s,force=False):
  if isinstance(s, QuoteEscapedString) and not force:
    return s
  elif isinstance(s, str):
    return QuoteEscapedString(s.replace('"', r"\"").replace("'", r"\'"))
  else:
    return QuoteEscapedString(str(s).replace('"', r"\"").replace("'", r"\'"))

class InvalidHtmlTagUse(Exception): pass

# Consider HTML escaping?
class HtmlTag(Element):
  """An HTML tag. See __init__ docstring for details on use."""

  @staticmethod
  def render(tag):
    return '\n'.join(HtmlTag._walk(tag, [], 0))

  @staticmethod
  def _walk(tag, elements, depth):
    for e in tag:
      if isinstance(e, Generator):
        HtmlTag._walk(e, elements, depth+1)
      else:
        elements.append(("  " * depth) + str(e))
    return elements

  def __init__(self, tag_name, class_=None, text="", **kwargs):
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

    self.tag_name = tag_name
    self.inner_text = text
    self.fields = kwargs
    if class_ is not None:
      self.fields['class'] = class_

  # Used for stand-alone tag for tags without children
  def __str__(self):
    return self._open_tag() + self.inner_text + self._close_tag()

  # Used for decorator syntax for tags with children
  def __call__(self, method):
    if self.inner_text:
      raise InvalidHtmlTagUse("Body text cannot be specified for a decorator HtmlTag")
    def wrapper(*args):
      yield self._open_tag()
      yield method(*args)
      yield self._close_tag()
    wrapper.orig = method
    return wrapper

  # Wraps own formatting around some text
  def text(self, text):
    if self.inner_text:
      print >> sys.stderr, "Inner text is", self.inner_text
      raise InvalidHtmlTagUse("Cannot wrap formatting with existing text around new text")
    self.inner_text = text
    s = str(self)
    self.inner_text = None
    return s

  # Constructs the opening HTML tag for this TAG
  # @return String
  def _open_tag(self):
    '''Creates the opening tag for this element'''
    s = "<%s " % (self.tag_name,)
    s += " ".join(["%s=%s" % (str(key), str(val)) for key, val in self.fields.iteritems()])
    s += ">"
    return s

  # Constructs the closing HTML tag for this HtmlTag
  # @return String
  def _close_tag(self):
    '''Returns the closing tag for this element'''
    return "</%s>" % (self.tag_name,)

# ###################################################################
# PRE-DEFINED CLASSES
# ###################################################################

# Self-closing tags
class area(HtmlTag):
  def __init__(self, **kwargs):
    super(area, self).__init__("area", self_closing=True, **kwargs)
class base(HtmlTag):
  def __init__(self, **kwargs):
    super(base, self).__init__("base", self_closing=True, **kwargs)
class br(HtmlTag):
  def __init__(self, **kwargs):
    super(br, self).__init__("br", self_closing=True, **kwargs)
class col(HtmlTag):
  def __init__(self, **kwargs):
    super(col, self).__init__("col", self_closing=True, **kwargs)
class embed(HtmlTag):
  def __init__(self, **kwargs):
    super(embed, self).__init__("embed", self_closing=True, **kwargs)
class frame(HtmlTag):
  def __init__(self, **kwargs):
    super(frame, self).__init__("frame", self_closing=True, **kwargs)
class hr(HtmlTag):
  def __init__(self, **kwargs):
    super(hr, self).__init__("hr", self_closing=True, **kwargs)
class img(HtmlTag):
  def __init__(self, **kwargs):
    super(img, self).__init__("img", self_closing=True, **kwargs)
class input(HtmlTag):
  def __init__(self, **kwargs):
    super(input, self).__init__("input", self_closing=True, **kwargs)
class link(HtmlTag):
  def __init__(self, **kwargs):
    super(link, self).__init__("link", self_closing=True, **kwargs)
class meta(HtmlTag):
  def __init__(self, **kwargs):
    super(meta, self).__init__("meta", self_closing=True, **kwargs)
class param(HtmlTag):
  def __init__(self, **kwargs):
    super(param, self).__init__("param", self_closing=True, **kwargs)

class a(HtmlTag):
  def __init__(self, **kwargs):
    super(a, self).__init__("a", inline=True, **kwargs)
class abbr(HtmlTag):
  def __init__(self, **kwargs):
    super(abbr, self).__init__("abbr", **kwargs)
class acronym(HtmlTag):
  def __init__(self, **kwargs):
    super(acronym, self).__init__("acronym", **kwargs)
class address(HtmlTag):
  def __init__(self, **kwargs):
    super(address, self).__init__("address", **kwargs)
class article(HtmlTag):
  def __init__(self, **kwargs):
    super(article, self).__init__("article", **kwargs)
class aside(HtmlTag):
  def __init__(self, **kwargs):
    super(aside, self).__init__("aside", **kwargs)
class audio(HtmlTag):
  def __init__(self, **kwargs):
    super(audio, self).__init__("audio", **kwargs)

class b(HtmlTag):
  def __init__(self, **kwargs):
    super(b, self).__init__("b", inline=True, **kwargs)
class bdo(HtmlTag):
  def __init__(self, **kwargs):
    super(bdo, self).__init__("bdo", **kwargs)
class big(HtmlTag):
  def __init__(self, **kwargs):
    super(big, self).__init__("big", **kwargs)
class blockquote(HtmlTag):
  def __init__(self, **kwargs):
    super(blockquote, self).__init__("blockquote", **kwargs)
class body(HtmlTag):
  def __init__(self, **kwargs):
    super(body, self).__init__("body", **kwargs)
class button(HtmlTag):
  def __init__(self, **kwargs):
    super(button, self).__init__("button", inline=True, **kwargs)

class canvas(HtmlTag):
  def __init__(self, **kwargs):
    super(canvas, self).__init__("canvas", **kwargs)
class caption(HtmlTag):
  def __init__(self, **kwargs):
    super(caption, self).__init__("caption", **kwargs)
class center(HtmlTag):
  def __init__(self, **kwargs):
    super(center, self).__init__("center", **kwargs)
class cite(HtmlTag):
  def __init__(self, **kwargs):
    super(cite, self).__init__("cite", **kwargs)
class code(HtmlTag):
  def __init__(self, **kwargs):
    super(code, self).__init__("code", **kwargs)
class colgroup(HtmlTag):
  def __init__(self, **kwargs):
    super(colgroup, self).__init__("colgroup", **kwargs)
class command(HtmlTag):
  def __init__(self, **kwargs):
    super(command, self).__init__("command", **kwargs)

class datalist(HtmlTag):
  def __init__(self, **kwargs):
    super(datalist, self).__init__("datalist", **kwargs)
class dd(HtmlTag):
  def __init__(self, **kwargs):
    super(dd, self).__init__("dd", **kwargs)
class details(HtmlTag):
  def __init__(self, **kwargs):
    super(details, self).__init__("details", **kwargs)
class dfn(HtmlTag):
  def __init__(self, **kwargs):
    super(dfn, self).__init__("dfn", **kwargs)
class dialog(HtmlTag):
  def __init__(self, **kwargs):
    super(dialog, self).__init__("dialog", **kwargs)
class div(HtmlTag):
  def __init__(self, **kwargs):
    HtmlTag.__init__(self, "div", **kwargs)
class dl(HtmlTag):
  def __init__(self, **kwargs):
    super(dl, self).__init__("dl", **kwargs)
class dt(HtmlTag):
  def __init__(self, **kwargs):
    super(dt, self).__init__("dt", **kwargs)

class em(HtmlTag):
  def __init__(self, **kwargs):
    super(em, self).__init__("em", **kwargs)

class fieldset(HtmlTag):
  def __init__(self, **kwargs):
    super(fieldset, self).__init__("fieldset", **kwargs)
class figure(HtmlTag):
  def __init__(self, **kwargs):
    super(figure, self).__init__("figure", **kwargs)
class footer(HtmlTag):
  def __init__(self, **kwargs):
    super(footer, self).__init__("footer", **kwargs)
class form(HtmlTag):
  def __init__(self, **kwargs):
    super(form, self).__init__("form", **kwargs)
class frameset(HtmlTag):
  def __init__(self, **kwargs):
    super(frameset, self).__init__("frameset", **kwargs)

class h1(HtmlTag):
  def __init__(self, **kwargs):
    super(h1, self).__init__("h1", **kwargs)
class h2(HtmlTag):
  def __init__(self, **kwargs):
    super(h2, self).__init__("h2", **kwargs)
class h3(HtmlTag):
  def __init__(self, **kwargs):
    super(h3, self).__init__("h3", **kwargs)
class h4(HtmlTag):
  def __init__(self, **kwargs):
    super(h4, self).__init__("h4", **kwargs)
class h5(HtmlTag):
  def __init__(self, **kwargs):
    super(h5, self).__init__("h5", **kwargs)
class h6(HtmlTag):
  def __init__(self, **kwargs):
    super(h6, self).__init__("h6", **kwargs)
class head(HtmlTag):
  def __init__(self, **kwargs):
    super(head, self).__init__("head", **kwargs)
class header(HtmlTag):
  def __init__(self, **kwargs):
    super(header, self).__init__("header", **kwargs)
class hgroup(HtmlTag):
  def __init__(self, **kwargs):
    super(hgroup, self).__init__("hgroup", **kwargs)
class html(HtmlTag):
  def __init__(self, **kwargs):
    super(html, self).__init__("html", **kwargs)

class i(HtmlTag):
  def __init__(self, **kwargs):
    super(i, self).__init__("i", inline=True, **kwargs)
class iframe(HtmlTag):
  def __init__(self, **kwargs):
    super(iframe, self).__init__("iframe", **kwargs)
class ins(HtmlTag):
  def __init__(self, **kwargs):
    super(ins, self).__init__("ins", **kwargs)
class keygen(HtmlTag):
  def __init__(self, **kwargs):
    super(keygen, self).__init__("keygen", **kwargs)
class kbd(HtmlTag):
  def __init__(self, **kwargs):
    super(kbd, self).__init__("kbd", **kwargs)
class label(HtmlTag):
  def __init__(self, **kwargs):
    super(label, self).__init__("label", **kwargs)
class legend(HtmlTag):
  def __init__(self, **kwargs):
    super(legend, self).__init__("legend", **kwargs)
class li(HtmlTag):
  def __init__(self, **kwargs):
    super(li, self).__init__("li", **kwargs)

class map(HtmlTag):
  def __init__(self, **kwargs):
    super(map, self).__init__("map", **kwargs)
class mark(HtmlTag):
  def __init__(self, **kwargs):
    super(mark, self).__init__("mark", **kwargs)
class meter(HtmlTag):
  def __init__(self, **kwargs):
    super(meter, self).__init__("meter", **kwargs)
class nav(HtmlTag):
  def __init__(self, **kwargs):
    super(nav, self).__init__("nav", **kwargs)
class noframes(HtmlTag):
  def __init__(self, **kwargs):
    super(noframes, self).__init__("noframes", **kwargs)
class noscript(HtmlTag):
  def __init__(self, **kwargs):
    super(noscript, self).__init__("noscript", **kwargs)

class ol(HtmlTag):
  def __init__(self, **kwargs):
    super(ol, self).__init__("ol", **kwargs)
class optgroup(HtmlTag):
  def __init__(self, **kwargs):
    super(optgroup, self).__init__("optgroup", **kwargs)
class option(HtmlTag):
  def __init__(self, **kwargs):
    super(option, self).__init__("option", **kwargs)
class p(HtmlTag):
  def __init__(self, **kwargs):
    super(p, self).__init__("p", **kwargs)
class pre(HtmlTag):
  def __init__(self, **kwargs):
    super(pre, self).__init__("pre", **kwargs)
class progress(HtmlTag):
  def __init__(self, **kwargs):
    super(progress, self).__init__("progress", **kwargs)

class q(HtmlTag):
  def __init__(self, **kwargs):
    super(q, self).__init__("q", **kwargs)
class ruby(HtmlTag):
  def __init__(self, **kwargs):
    super(ruby, self).__init__("ruby", **kwargs)
class rt(HtmlTag):
  def __init__(self, **kwargs):
    super(rt, self).__init__("rt", **kwargs)
class rp(HtmlTag):
  def __init__(self, **kwargs):
    super(rp, self).__init__("rp", **kwargs)

class s(HtmlTag):
  def __init__(self, **kwargs):
    super(s, self).__init__("s", **kwargs)
class samp(HtmlTag):
  def __init__(self, **kwargs):
    super(samp, self).__init__("samp", **kwargs)
class script(HtmlTag):
  def __init__(self, **kwargs):
    super(script, self).__init__("script", **kwargs)
class section(HtmlTag):
  def __init__(self, **kwargs):
    super(section, self).__init__("section", **kwargs)
class select(HtmlTag):
  def __init__(self, **kwargs):
    super(select, self).__init__("select", inline=True, **kwargs)
class small(HtmlTag):
  def __init__(self, **kwargs):
    super(small, self).__init__("small", inline=True, **kwargs)
class source(HtmlTag):
  def __init__(self, **kwargs):
    super(source, self).__init__("source", **kwargs)
class span(HtmlTag):
  def __init__(self, **kwargs):
    super(span, self).__init__("span", inline=True, **kwargs)
class strike(HtmlTag):
  def __init__(self, **kwargs):
    super(strike, self).__init__("strike", **kwargs)
class strong(HtmlTag):
  def __init__(self, **kwargs):
    super(strong, self).__init__("strong", **kwargs)
class style(HtmlTag):
  def __init__(self, **kwargs):
    super(style, self).__init__("style", **kwargs)
class sub(HtmlTag):
  def __init__(self, **kwargs):
    super(sub, self).__init__("sub", **kwargs)
class sup(HtmlTag):
  def __init__(self, **kwargs):
    super(sup, self).__init__("sup", **kwargs)

class table(HtmlTag):
  def __init__(self, **kwargs):
    super(table, self).__init__("table", **kwargs)
class tbody(HtmlTag):
  def __init__(self, **kwargs):
    super(tbody, self).__init__("tbody", **kwargs)
class td(HtmlTag):
  def __init__(self, **kwargs):
    super(td, self).__init__("td", **kwargs)
class textarea(HtmlTag):
  def __init__(self, **kwargs):
    super(textarea, self).__init__("textarea", inline=True, **kwargs)
class tfoot(HtmlTag):
  def __init__(self, **kwargs):
    super(tfoot, self).__init__("tfoot", **kwargs)
class th(HtmlTag):
  def __init__(self, **kwargs):
    super(th, self).__init__("th", **kwargs)
class thead(HtmlTag):
  def __init__(self, **kwargs):
    super(sup, self).__init__("sup", **kwargs)
class time(HtmlTag):
  def __init__(self, **kwargs):
    super(time, self).__init__("time", **kwargs)
class title(HtmlTag):
  def __init__(self, **kwargs):
    super(title, self).__init__("title", **kwargs)
class tr(HtmlTag):
  def __init__(self, **kwargs):
    super(tr, self).__init__("tr", **kwargs)
class tt(HtmlTag):
  def __init__(self, **kwargs):
    super(tt, self).__init__("tt", **kwargs)

class u(HtmlTag):
  def __init__(self, **kwargs):
    super(u, self).__init__("u", **kwargs)
class ul(HtmlTag):
  def __init__(self, **kwargs):
    super(ul, self).__init__("ul", **kwargs)
class var(HtmlTag):
  def __init__(self, **kwargs):
    super(var, self).__init__("var", **kwargs)
class video(HtmlTag):
  def __init__(self, **kwargs):
    super(video, self).__init__("video", **kwargs)
