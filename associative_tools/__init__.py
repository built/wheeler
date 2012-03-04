"""
Associative Tools is a small collection of classes created during the development of the Wheeler programming language.
"""

import functools

class AssociativeSet():
	"""
	AssociativeSet is a hashed (associative) set that can contain other sets. It also provides tooling to create
	relations between AssociativeSets, effectively letting you create arbitrary data structures (graphs) with sets.

	Each AssociativeSet can serve as a context for creating and managing relationships among other sets.
	"""
	def __init__(self, name):
		self.name = name
		self.contents = {}
		self.counter = 0

	def add(self, *named_sets):
		for named_set in named_sets:
			self.contents[named_set.name] = named_set

	def __len__(self):
		return len(self.contents)

	def connect(self, named_set):
		self.add(named_set)
		named_set.add(self)

	def disconnect(self, named_set):
		del self.contents[named_set.name]
		del named_set.contents[self.name]

	def __contains__(self, item):
		return (item in self.contents)

	def comprehend(self, *item_names):
		"""
		Returns any intersections between the given items. These intersections are often relations created by associate().
		"""
		given = []
		negated = []

		for name in item_names:
			negated.append(name[1:]) if name.startswith('!') else given.append(name)

		negated_items = set(self.lookup_items_by_name(*negated))
		given_items = set(self.lookup_items_by_name(*given))
		intersection = self.related(given_items) - given_items - self.related(negated_items)
		return list(intersection)

	def create_relation(self, basename=None):
		"""
		Creates an AssociativeSet in the current context that is solely for the purpose of
		describing a relationship between two other AssociativeSets.
		Relations have a name automatically created for them, usually of the form:
		__relation__0, where the number serves to uniquely identify the relation in the
		given context. You can have the relations take on a slightly different form by
		providing your own basename. For example, a basename of "category" would have a
		name of the form __category__0.
		"""
		relation = AssociativeSet("__%s__%s" % (basename or "relation", self.counter) )
		relation.connect(self)
		self.counter += 1
		return relation

	def related(self, criteria):
		if len(criteria) < 1: return set()
		return set.intersection(*[set(c.contents.values()) for c in criteria]) - set([self])

	def lookup_items_by_name(self, *names):
		return [self.contents[name] if name in self else AssociativeSet(name) for name in names]

	def associate(self, *items):
		"""
		The star of the show. Associates all of the items given (usually strings).
		"""
		items = self.lookup_items_by_name(*items)
		self.add(*items)
		relation = self.create_relation()
		[relation.connect(item) for item in items]

	def disassociate(self, *items):
		"""
		Disconnects all relations between the items given (usually strings).
		"""
		for relation in self.comprehend(*items):
			for item in self.lookup_items_by_name(*items):
				relation.disconnect(item)
			self.disconnect(relation)

	def matches(this_pattern, possible_match):
		return possible_match.name == this_pattern.name

	def describes(this_pattern, possible_match):
		if len(this_pattern.contents) < 1 and len(possible_match.contents) > 0: return False


		misses = [item for item in this_pattern.contents.values() if item.name not in possible_match.contents.keys()]
		return len(misses) < 1

	def list_terms(self):
		return self.contents.keys()
	terms = property(list_terms)
