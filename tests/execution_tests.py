import unittest
from category import *
from category.stdout import *
from interpreter.tools import parse, evaluate

class TestExecution(unittest.TestCase):

	def test_evaluate_atom(self):
		pass #TODO
		# 
		# root = Category('*')
		# 
		# # Relate "foo" and "bar"
		# evaluate(parse("foo bar", root), root)
		# 
		# # Verify they are related
		# foo = root.contents["foo"]
		# bar = root.contents["bar"]
		# 
		# self.assertTrue(bar.related(set([foo])), "We need 'foo' and 'bar' to be related for this test.")
		# 
		# # Disassociate them.
		# evaluate(parse("<> foo bar", root), root)
		# 
		# # Verify they are no longer related.
		# self.assertFalse(bar.related(set([foo])), "The relationship between 'foo' and 'bar' still exists.")

	#
	# LAW DON'T GO ROUND HERE, LAW DOG!
	# (Come back to this one later.)
	# def test_simultaneous_transitions(self):
	# 	root = Category('*')
	# 
	# 	setup_expressions = [
	# 		"transition (pattern (A qualifier)) (action B)",
	# 		"transition (pattern (Y qualifier)) (action Z)",
	# 		"foo A",
	# 		"bar B"
	# 	]
	# 
	# 	# Setup the world
	# 	for expression in setup_expressions:
	# 		evaluate(parse(expression, root), root)
	# 
	# 	expression = "foo bar"
	# 
	# 	# After evaluation the following relationships should exist:
	# 	# foo B
	# 	# bar Z
	# 	# foo bar
	# 	expected_relationships = [
	# 		"foo B",
	# 		"bar Z",
	# 		"foo bar"
	# 	]
	# 	
	# 	relationships = [ root.comprehend(*r.split()) for r in expected_relationships ]
	# 
	# 	# Verify those relationships do not yet exist.
	# 	self.assertFalse(any(relationships), "None of those relationships should exist yet.")
	# 
	# 	evaluate(parse(expression, root), root)
	# 	
	# 	# Now, ALL of those relationships should exist.
	# 	
	# 	relationships = [ root.comprehend(*r.split()) for r in expected_relationships ]
	# 	self.assertTrue(all(relationships), "All of those relationships should exist.")


if __name__ == '__main__':
    unittest.main()
