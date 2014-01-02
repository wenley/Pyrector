
class WidgetExternalsMixin(object):

  externals = []

  @classmethod
  def externals_list(self):
    ordered = []
    unique = set()
    for klass in self.__mro__:
      if issubclass(klass, Widget):
        for e in klass.externals:
          if e not in unique:
            ordered.append(e)
            unique.add(e)
    return ordered

  def include_externals(self):
    for external in self.externals_list():
      yield external

