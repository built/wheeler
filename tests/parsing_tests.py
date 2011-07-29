import unittest
from category import *
from interpreter.tools import syntax_tree, parse, categorize, categorized_expression
from associative_tools import AssociativeSet

class TestParsing(unittest.TestCase):

	def test_parse_nothing(self):
		root = Category()
		self.assertNotEqual( root, None)

	def test_syntax_tree_of_atom(self):
		expression = "foo"
		tree = syntax_tree(expression)
		self.assertTrue(isinstance(tree, list))
		self.assertEqual(tree, ['foo'])
	
	def test_syntax_tree_of_simple_expression(self):
		expression = "foo bar"
		tree = syntax_tree(expression)
		self.assertTrue(isinstance(tree, list))
		self.assertEqual(tree, ['foo', 'bar'])
	
	def test_creating_categorized_expression(self):
		context  = AssociativeSet("")
		categories = [Category("foo", context)]
		foo = categorized_expression(categories, context)
		self.assertEqual(foo.name, "__relation__0")
	
	def test_categorization_of_atom(self):
		expression = ['foo']
		context  = AssociativeSet("*")
		categorized = categorize(expression, context)
		self.assertEqual(AssociativeSet("__relation__0").name, categorized.name)
		# We expect a category related to the context we've created and our expression, 'foo'
		self.assertTrue("*" in categorized.contents)
		self.assertTrue("foo" in categorized.contents)
		# What categories should we get back, and in what structure?
		# "expr_000" <=> "foo"
	
	def test_parse_atom(self):
	
		root = AssociativeSet('.')
		expression = "foo"
		parsed = parse(expression, root)
	
		self.assertTrue( isinstance(parsed, AssociativeSet) )
		self.assertTrue( expression in parsed.contents, "Not seeing 'foo' in the contents.")
	
	
	def test_parse_simple_expression(self):
	
		root = AssociativeSet('.')
	
		expression = "foo bar"
	
		# Note that this is the result of the expression being
		# *parsed*, not *parsed AND evaluated*. If it was being
		# evaluated there would be another category that represented
		# the result of the interaction.
		expression_result = parse(expression, root)
	
		# Expected in root: foo, bar, the relation between them, and the literal <<relation>> category.
		# Also the ordinal values (positions) for each element of the expression, and a relation for each.
		# And the 'position' category.
		# self.assertEqual( len(root.contents), 9)
		self.assertTrue( "foo" in root.contents )
		self.assertTrue( "bar" in root.contents )
		self.assertTrue( "__relation__0" in root.contents )
	
	def test_parse_ordering_of_expression(self):
	
		root = AssociativeSet('*')
		expression_result = parse("foo bar", root)
		
		self.assertEqual(len(root.comprehend("foo", "0")), 1) # Should get ONE hit.
	
		position_relation = root.comprehend("foo", "0")[0]
		
		self.assertTrue("position" in position_relation.contents)
		
		position_tags = [x for x in position_relation.contents.values() if "position" in x.contents]
		self.assertTrue(position_tags, "Should be able to see the position relation marked as such.")

		# TODO: Restore some sort of test like this to reverse-lookup values.
		# position_relation = root.comprehend("position", "0")[0]
		# self.assertTrue("foo" in position_relation.contents, "Should be able look up our value from its position.")
	
	def test_parse_nested_expression(self):
	
		root = AssociativeSet('*')
	
		parse_text = "foo bar (baz berz)"
	
		parse(parse_text, root)
	
		# Expected: foo, bar, (baz berz), baz, berz, outer expression, inner expression (parenthetical)
		# Plus outer ordinals: 0, 1, 2 (which should be shared w/ inner ordinals) and 5 relations to
		# support them, and the 'position' category.
		# self.assertEqual( len(root.contents), 15)
	
		self.assertTrue( "foo" in root.contents )
		self.assertTrue( "bar" in root.contents )
	
		relations = root.comprehend("baz", "berz")
	
		self.assertTrue(len(relations) > 0, "Should get a relation back for the inner expression")
	
		inner_expression = relations[0]
	
		self.assertNotEqual( inner_expression.name, '*', "Shouldn't get root back as our match")
	
		self.assertTrue("baz" in inner_expression, "Can't see first item in nested expression.")
		self.assertTrue("berz" in inner_expression, "Can't see second item in nested expression.")
		# Expected categories: (FROM THE POINT OF VIEW OF THE INNER EXPRESSION, NOT ROOT)
		# Root, baz, berz, 'relation', ordinal for baz, ordinal for berz, containing expression, and the ordinal for the containing expression.
		# self.assertEqual( len(inner_expression.contents), 8)
	
	

if __name__ == '__main__':
    unittest.main()
