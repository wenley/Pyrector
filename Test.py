
def tag(meth):
  def wrap(*args, **kwargs):
    yield meth.__name__
    for text in meth(*args, **kwargs):
      yield text
    yield "close" + meth.__name__
  return (lambda : wrap())

class Test:
  """A test class"""

  __something = "aoeu"

  def __getattr__(self, name):
    try:
      super
    except e:
      print "Trying to access %s" % (name,)
      raise AttributeError("Accessing unknown attribute %s" % (name,))

  def foo(self):
    print "self.something is", self.something

  def bar(self):
    self.foo()
    print "something is ", self.__class__.__something

  @staticmethod
  def grep():
    print "Called grep"

  @tag
  def body(self):
    yield "something"
    @tag
    def div():
      yield str({'src': 'google link'})
    for text in div():
      yield text

  @classmethod
  def group(klass):
    print "Group called with class", klass

  def render(self):
    return "\n".join([text for text in self.body()])


class Subtest(Test):
  pass

if __name__ == "__main__":
  print "Running main of Test.py"
  Test.grep()
  Subtest.group()
  t = Test()
  t.bar()
  t.something
  print t.render()
