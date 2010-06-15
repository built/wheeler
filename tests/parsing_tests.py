import unittest
from category import *
from interpreter.tools import parse, rebuild_expression

class TestParsing(unittest.TestCase):

	def test_evaluate_nothing(self):

		root = Category()
		self.assertNotEqual( root, None)

	def test_evaluate_atom(self):

		root = Category('.')

		expression = "foo"

		self.assertEqual( type( parse(expression, root) ), Category)

		self.assertTrue( parse(expression, root).has(expression), "Not seeing 'foo' in the contents.")


	def test_evaluate_simple_expression(self):
	
		root = Category('.')
	
		expression = "foo bar"
	
		# Note that this is the result of the expression being
		# *parsed*, not *parsed AND evaluated*. If it was being 
		# evaluated there would be another category that represented
		# the result of the interaction.
		expression_result = parse(expression, root)
	
		# Expected: foo, bar, and (foo bar)
		self.assertEqual( len(root.contents), 3)
	
		self.assertTrue( "foo" in root.contents.keys() )
		self.assertTrue( "bar" in root.contents.keys() )
	
	
	def test_rebuild_expression(self):
		tokenization = ['foo', 'bar', ['abc', ['123'], 'foofy'], 'lalala']
		expected_expression = "(foo bar (abc (123) foofy) lalala)"
		actual_expression = rebuild_expression(tokenization)
		self.assertEqual(actual_expression, expected_expression, "\nExpect: ]%s[\nSeeing: ]%s[" % (expected_expression, actual_expression))
	
	def test_evaluate_nested_expression(self):
	
		root = Category('*')
	
		parse_text = "foo bar (baz berz)"
	
		parse(parse_text, root)

		# Expected: foo, bar, (baz berz), baz, berz, outer expression.
		self.assertEqual( len(root.contents), 6)
	
		self.assertTrue( "foo" in root.contents.keys() )
		self.assertTrue( "bar" in root.contents.keys() )
	
		self.assertTrue( '(baz berz)' in root.contents, "Can't see nested expression.")
	
		# Expected categories: baz, berz
		self.assertEqual( len(root.contents['(baz berz)'].contents), 2)
	
		self.assertTrue( "baz" in root.contents['(baz berz)'].contents.keys() )
		self.assertTrue( "berz" in root.contents['(baz berz)'].contents.keys() )
	
	

if __name__ == '__main__':
    unittest.main()
