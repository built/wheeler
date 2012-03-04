class FuzzyHash:
	"""
	FuzzyHash acts like a hashtable, except it lets you have "fuzzy" values for the keys.
	More precisely, it lets you specify a range as the key when you create the hash entry,
	and it lets you look that entry back up with any value that is in the range originally
	specified.
	"""
	
	# Challenges:
	# performance
	# Describing ranges
	# Describing asymmetric unbounded ranges (3 to infinity, etc.)
	# Non-integer keys and abstract (but still numeric) keys, ex: pi or e?
	# Could you have a revolving hash that triggers on multiples of pi? So cycling happens?
	
	def __init__(self):
		self.slots = []
	
	def __getitem__(self, key):
		for key_range, value in self.slots:
			if key in key_range:
				return value

	def __setitem__(self, key_range, value):
		self.slots += [(key_range, value)]
