
from html_tag import HtmlTag
from collections import defaultdict
from buffer import Buffer

def staticcontent(method):
  name = method.__name__
  def wrapper(self, *args, **kwargs):
    cached = self.cache_read(name)
    if cached:
      self.buffer.extend(cached)
    else:
      old = self.buffer
      self.buffer = Buffer()
      method(self, *args, **kwargs)

      self.cache_write(name, self.buffer)
      old.extend(self.buffer)
      self.buffer = old
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

