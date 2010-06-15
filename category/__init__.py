import re

ANYTHING = '.'
LAST_RESULT = '$_'

def islist(obj):
	return isinstance(obj, list)

def iscategory(obj):
	return isinstance(obj, Category)

def istoken(obj):
	return isinstance(obj, str)

def items_that_will_react(transition_name, category_list):

	if transition_name == ANYTHING: return category_list # Everything matches

	return [item for item in category_list if transition_name in item.family()]


class ContainingModuleNameGivenInsteadOfClassName:
	pass

class FeatureNotImplemented:
	pass

class CategoryRequired:
	pass

class Category(object):

	def __init__(self, expression="", given_context=None):

		self.context = given_context
		self.value = expression
		self.contents = {}
		self.transitions = {}

		# Register with context, if given AND if not already known.
		if given_context:
			if self.name not in given_context.contents:
				given_context.contents[self.name] = self
			else:
				raise "YOU ARE TRYING TO REDEFINE A CATEGORY w/ NAME: %s" % self.name


	def get_id(self):
		return self.__hash__()

	id = property(get_id)

	def get_name(self):
		return str(self.value)

	name = property(get_name)


	"""
	You can add a category or a list of categories.
	"""
	def add(self, addendum):
		results = []

		if islist(addendum):
			return [self.bulk_add(addendum)] if len(addendum) > 0 else []

		assert( iscategory(addendum) )

		self.register(addendum)

		reaction = self.react(addendum)

		return results + [reaction] if reaction else results

	def bulk_add(self, addendum):
		assert( isinstance(addendum, list) )

		for category in addendum:
			self.register(addendum)

		reaction = self.react(addendum)

		return reaction


	def register(self, addendum):

		if iscategory(addendum):
			self.contents[addendum.name] = addendum
		elif islist(addendum):
			# if self.name == "+":
			# 	print "Registering for + : %s" % [a.name for a in addendum]

			for item in addendum:
				self.register(item)
		else:
			raise "I DON'T KNOW WHAT YOU ARE. (%s Can only init with a category or list of categories." % type(addendum)

	def peers(self, other_categories):
		""" Given a list of categories, remove self from that list and return it. """
		return [category for category in other_categories if category != self]

	def evaluate(self):
		results = []

		# Let the categories interact.
		# Interactions are awesome!
		for category in self.contents.values():
			results += category.add( category.peers(self.contents.values() ) )

		# Remember this result.
		if LAST_RESULT in self.contents:
			print "About to remove: %s" % self.contents[LAST_RESULT]
			self.remove(LAST_RESULT)
		final_result = self.create(LAST_RESULT)
		final_result.add(results)

		return final_result

	def react(self, items_being_added):
		if iscategory(items_being_added) and items_being_added.name == LAST_RESULT: return [] # Ignore $_

		if not islist(items_being_added): items_being_added = [items_being_added]

		# Look at each transition that we have and then select
		# the best matching categories for each.
		# Then execute those transitions.
		return [self.transitions[transition](items_that_will_react(transition, items_being_added)) for transition in self.transitions]


	def has_transition_for(self, category_name):
		return category_name in self.transitions


	"""
	Returns a set of this category's "family".
	Family is determined by inherent type (name) or first-order type (contents).
	"""
	def family(self):
		return set( [self.name] + [ cat.name for cat in self.contents.values() if cat.name != LAST_RESULT] + ['.'])


	def add_handler(self, category, transition):
		self.transitions[category.name] = transition


	def has(self, category):
		return category in self.contents


	def remove(self, category_name):
		if category_name in self.contents:
			del self.contents[category_name]


	def dump(self, file):
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
		print "Name: %s" % self.name
		print "ID: %s"  % self.id
		
		if not self.contents:
			print "%s doesn't have content." % self.name
			file.write(self.name + ";\n")
			file.write("}\n")
			return
		else:
			file.write(self.name + ";\n")

		for key in self.contents:
			file.write("%s--%s;\n" % (self.name, self.contents[key].name) )
			print "DUMPING TO DOT FILE: %s--%s;" % (self.name, self.contents[key].name)
		for category_name in self.transitions:
			print " @ %s" % (category_name)
		else:
			print "No transitions."

		print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"


	def join_context(self, given_context):
		if self.context == given_context:
			return
		self.context = given_context
		for related in self.contents.values():
			related.join_context(given_context);

		for related in self.transitions.values():
			print "Going to make %s join %s" % (related.name, self.name)
			related.join_context(given_context);


	def create(self, name):
		"""
		Create a category within the context of *this* category.
		"""
		return self.contents[name] if name in self.contents else Category(name, self)












