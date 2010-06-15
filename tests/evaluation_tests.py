import unittest
from category import *
from category.stdout import *
from interpreter.tools import parse

class TestParsing(unittest.TestCase):

	def test_evaluate_nothing(self):
	
		root = Category()
		self.assertNotEqual( root, None)
	
	
	def test_evaluate_atom(self):
	
		root = Category('*')
		
		expression = "foo"
	
		parse(expression, root).evaluate()
		
		self.assertEqual( len(root.contents), 2) # "foo" + container (but not $_, as ROOT was not evaluated.
		
		self.assertTrue( "foo" in root.contents.keys() )
	
		self.assertTrue( root.has("foo") )
	
		self.assertTrue( isinstance( root.contents["foo"], Category) )

	def test_evaluate_simple_expression(self):
	
		root = Category('*')

		stdout = Category("stdout", root)
	
		expression = 'stdout "foo"'
	
		result = parse(expression, root).evaluate()
		
		category_stdout = root.contents['stdout']

		category_foo = root.contents['"foo"']
		
		self.assertFalse('(stdout "foo")' in category_foo.contents, "Why is a nested expression appearing here?")
		
		self.assertTrue('stdout' in category_foo.contents)
		
		self.assertTrue('"foo"' in category_stdout.contents)

	# def test_evaluate_simple_expression(self):
	# 
	# 	root = Category('*')
	# 
	# 	expression = "2 + 3"
	# 
	# 	result = parse(expression, root).evaluate()
	# 
	# 	# Expected categories are 2, +, and 3
	# 	self.assertEqual( len(root.contents), 3)
	# 	
	# 	self.assertEqual( type(result), type(Category()))
	# 	
	# 	self.assertTrue(result.has(3), "%s isn't %s" % (result.name, Category(3, root).name))


if __name__ == '__main__':
    unittest.main()
