import unittest
from category import *
from category.stdout import *
from interpreter.tools import parse, evaluate

class TestEvaluation(unittest.TestCase):

	def test_evaluate_atom(self):

		root = Category('*')
		root.create("relation") # Housekeeping

		expression = "foo"

		parsed = parse(expression, root)

		evaluate(parsed, root)

		# After an evaluation we should be able to see a relation which represents the result
		# of this particular evaluation. It will relate to a timestamp and the given expression.
		# In this way you should be able to see a history of evaluations.

		self.assertTrue( "foo" in root.contents.keys() )

		self.assertTrue( root.has("foo") )

		self.assertTrue( isinstance( root.contents["foo"], Category) )

		foo = root.contents["foo"]

		self.assertFalse(foo.has("relation")) # Should not connect directly to <<relation>>


	def test_evaluate_simple_expression(self):

		root = Category('*')

		expression = "foo bar baz"

		evaluate(parse(expression, root), root)  # Don't forget that at this point there are a bunch of meta-categories.

		connections = root.comprehend("baz", "foo", "bar")

		self.assertEqual(len(connections), 1) # Should just have the expression.


	def test_evaluate_simple_expression_multiple_times(self):

		root = Category('*')

		expression = "foo bar baz"

		evaluate(parse(expression, root), root)  # Don't forget that at this point there are a bunch of meta-categories.
		evaluate(parse(expression, root), root)  # Don't forget that at this point there are a bunch of meta-categories.
		evaluate(parse(expression, root), root)  # Don't forget that at this point there are a bunch of meta-categories.

		connections = root.comprehend("baz", "foo", "bar")

		self.assertEqual(len(connections), 3) # Should have a relation for each evaluation.
		
		# NO! Should only have a single relation for the connection. There should be metadata associated with each interaction instance.



	def test_evaluate_different_atoms(self):

		rootA = Category('*')
		rootB = Category('*')

		expressionA = "foo"
		expressionB = "(foo)"

		evaluate(parse(expressionA, rootA), rootA)
		evaluate(parse(expressionB, rootB), rootB)
		category_delta = len(rootB.contents) - len(rootA.contents)

		self.assertTrue(category_delta > 0, "Second expression should generate different numbers of categories")


if __name__ == '__main__':
    unittest.main()
