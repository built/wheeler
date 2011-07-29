from category_inspector import CategoryInspector
from associative_tools import AssociativeSet

class Category(AssociativeSet):

	def __init__(self, expression="", context=None):

		AssociativeSet.__init__(self, expression)

		if context:
			self.context = context
			context.connect(self)

	def has(self, category):
		return category in self.contents

	def dump(self, filename):
		if not file: return
		CategoryInspector(self).dump_to_file(filename)

	def create(self, name):
		cat = self.contents[name] if name in self.contents else Category(name, self)
		self.connect(cat)
		return cat
