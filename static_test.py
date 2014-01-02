
class Foo(object):

  static = []

  @staticmethod
  def is_static(method):
    static.append(method)
    return method

  @is_static
  def head(self):
    return "head"

class Bar(Foo):

  @Foo.is_static
  def head(self):
    return "bar head"

  @Foo.is_static
  def body(self):
    return "bar body"
