from category import *

def printer(category):
	if not isinstance(category, list):
		category = [category]
		
	for item in category:
		print item.name[1:-1],
	# stdout.remove(category.name)
	print
	return []

def line_printer(category):
	if not isinstance(category, list):
		category = [category]

	for item in category:
		print item.name[1:-1]
	# stdout.remove(category.name)
	return []


# It would be OUTSTANDING to be able to add a transition based on the absence of a category.
# For example, to say "for any category that isn't a list do(x)"
# We should be able to do that with the "not" category, to create an implicit category that doesn't match.
