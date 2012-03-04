class FuzzyHash
	
	# Challenges:
	# performance
	# Describing ranges
	# Describing asymmetric unbounded ranges (3 to infinity, etc.)
	# Non-integer keys and abstract (but still numeric) keys, ex: pi or e?
	# Could you have a revolving hash that triggers on multiples of pi? So cycling happens?
	
	def initialize:
		@slots = []
	
	def [](key):
	  @slots.detect { |key_range, value| key_range.include? key }

	def []=(key_range, value):
		@slots += [(key_range, value)]

end
