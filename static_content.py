
from html_tag import HtmlTag
from collections import defaultdict

def staticcontent(method):
  name = method.__name__
  def wrapper(self, *args):
    cached = self.cache_read(name)
    if cached:
      return cached
    else:
      cached = HtmlTag.render(method(self, *args))
      self.cache_write(name, cached)
      return cached
  return wrapper

class WidgetCacheMixin(object):
  """
  Mixin that performs caching operations for Widget.

  Controls reading and writing to the class-level cache.
  """
  _cache = defaultdict(lambda: None)
  @classmethod
  def cache_read(klass, name):
    return klass._cache[name]
  @classmethod
  def cache_write(klass, name, val):
    klass._cache[name] = val

