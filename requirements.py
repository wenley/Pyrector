
from django.template.base import VariableDoesNotExist

class WidgetRequirementsMixin(object):

  required = []

  @classmethod
  def requirements(self):
    return set([r for klass in self.__mro__ if issubclass(klass , Widget) for r in klass.required])

  def verify_requirements(self, context):
    missing = [key for key in self.requirements() if key not in context]
    if missing:
      raise VariableDoesNotExist("%s requires variables %s to render" %
          (self.__class__.__name__, ', '.join(missing)))

