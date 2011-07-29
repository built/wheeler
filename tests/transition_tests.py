import unittest
from category import *
from category.stdout import *
from interpreter.tools import *
from category import CategoryInspector

TRACK_TEST_CALLS = False

class TestTransitions(unittest.TestCase):
	def test_non_transition(self):
		root = Category('*')
		non_transition_expression = "foo bar"
		parsed = parse(non_transition_expression, root)
		evaluate(parsed, root )

	def test_transition_shape_after_parse(self):
		root = Category('*')

		# When category 'foo' interacts with category 'bar', it moves category
		# 'baz' into 'target'.
		transition_expression = "transition (pattern foo bar) (action baz target)"

		parsed_transition = parse(transition_expression, root)

		self.assertTrue('transition' in root)

		self.assertEqual( len(root.comprehend("foo", "bar", "pattern")), 1)

	def test_action_structure_in_defined_transition(self):
		root = Category('*')

		transition_expression = "transition (pattern foo bar) (action baz target)"

		evaluate(parse(transition_expression, root), root) # Defines the transition

		action_relations = root.comprehend('action', 'target', 'baz')
		self.assertEqual( len(action_relations), 1, "Should have one action")

		pattern_relations = root.comprehend('pattern', 'foo', 'bar')
		self.assertEqual( len(pattern_relations), 1, "Should have one pattern")

	def test_simplest_program(self):
		root = Category('*')
		term = "works"
		evaluate(parse(term, root), root )

		# Define a transition that detects when something enters "foo". That 'something' should be connected to "bar".
		transition = "transition (pattern foo (* qualifier) ) (action bar)"
		evaluate(parse(transition, root), root)

		matches = root.comprehend("bar", "works")
		self.assertEqual(len(matches), 0, "Shouldn't have a relationship between these yet.")

		expression = "foo works"
		evaluate(parse(expression, root), root )

		matches = root.comprehend("bar", "works")

		self.assertTrue(len(matches) > 0, "Did the transition fire? These two categories should be connected.")


	def test_transition_execution(self):

		root = Category('*')

		# define our transition
		evaluate( parse("transition (pattern foo bar) (action baz target)", root), root )

		# execute our transition
		evaluate( parse("foo bar", root), root )

		result = root.comprehend("baz", "target")

		self.assertTrue(len(result) > 1)


	# DRAGONS!!
	# def test_typed_transition(self):
	# 	root = Category('*')
	#
	# 	# term = '"example"'
	# 	term = "example string" # "example" is a string. Eventually just saying "example" should be equivalent.
	# 	evaluate(parse(term, root), root )
	#
	# 	# If you see a string, process it by putting it in the "processed" category.
	# 	transition = "transition (pattern (string qualifier)) (action processed)"
	# 	evaluate(parse(transition, root), root)
	#
	#
	# 	matches = root.comprehend("example", "processed")
	# 	self.assertEqual(len(matches), 0, "Shouldn't have a relationship between these yet.")
	#
	# 	expression = "example" # This should be enough to fire the transition.
	# 	evaluate(parse(expression, root), root )
	#
	# 	# Verify the result.
	# 	# matches = root.comprehend("example", "processed")
	# 	matches = [cat for cat in root.comprehend("example", "processed") if 'position' not in cat.contents]
	#
	# 	# CategoryInspector(root).dump_to_file('typed_transitions_2.dot')
	#
	# 	self.assertTrue(len(matches) > 0, "Did the transition fire? 'example' should be in 'processed' now.")

if __name__ == '__main__':
    unittest.main()










