
class Buffer(object):

  spaces_per_indent = 2

  def __init__(self):
    self.buf = []
    self.indentation = 0

  def __iter__(self):
    return self.buf.__iter__()

  def spaces(self):
    return ' ' * self.spaces_per_indent * self.indentation

  def append(self, el):
    self.buf.append(self.spaces() + str(el))

  def extend(self, els):
    self.buf.extend(self.spaces() + str(el) for el in els)

  def inline(self, el):
    self.buf[-1] += str(el)

  def indent(self):
    self.indentation += 1
  def unindent(self):
    self.indentation -= 1
    assert(self.indentation >= 0)
