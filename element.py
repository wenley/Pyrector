
from types import GeneratorType as Generator

class Element(object):

  @classmethod
  def render(cls, element):
    return '\n'.join(element._walk([], 0))

  @staticmethod
  def _generator_walk(gen, pieces, depth, add):
    for e in gen:
      if isinstance(e, Element):
        e._walk(elements, depth+1)
      elif isinstance(e, Generator):
        Element._generator_walk(e, pieces, depth)
      else:
        pieces.append(add(e, depth))

  def _walk(self, pieces, depth):
    for e in self:
      if isinstance(e, Element):
        e._walk(elements, depth+1)
      elif isinstance(e, Generator):
        Element._generator_walk(e, pieces, depth, e.add)
      else:
        self.add(pieces, e, depth)

  def __call__(self, method):
    def wrapper(*args):
      yield method(*args)
    return wrapper

  @staticmethod
  def generator_add(gen, buffer, depth):
    for e in gen:
      if isinstance(e, Element):
        e.add(buffer, depth+1)
      elif isinstance(e, Generator):
        Element.generator_add(e, buffer, depth)
      else:
        buffer.append(str(e))

  def add(self, buffer, depth):
    for sub in self:
      if isinstance(sub, Element):
        sub.add(buffer, depth+1)
      elif isinstance(sub, Generator):
        Element.generator_add(sub, buffer, depth)
      else:
        buffer.append(str(sub))

