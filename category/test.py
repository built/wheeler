from category import *

# This is part of a TEST category for testing purposes only.
# In our tests we'll be expected to make changes

def tester(category):
	first_item = category[0] if isinstance(category, list) and len(category) > 0 else category
	context = first_item.context
	context.create("TESTER_CALLED")
	return []
