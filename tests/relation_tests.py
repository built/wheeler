import unittest
from category import *
from interpreter.tools import create_relation, tokenize

class RelationParsing(unittest.TestCase):

	pass

	def test_create_basic_relation(self):

	 	root = Category('*')

		relation_expression = "x = 1 + 2"

	# 	relation = create_relation( tokenize("foo"), root)
	#
	# 	self.assert_(len(relation) > 0, "Our relation is empty? Really?")
	#
	# 	self.assertEqual(type(relation[0]), type(Category()), "Relation items must be Categories")
	#
	# 	self.assert_("foo" in [item.name for item in relation], "Can't find the item we added. ('foo')")
	#
	#
	# def test_create_nested_relation(self):
	#
	# 	expression = "foo (2 + 3)"
	#
	#  	root = Category('*')
	#
	# 	relation = create_relation( tokenize(expression), root)
	#
	# 	print tokenize(expression)
	#
	# 	self.assert_(len(relation) > 0, "Our relation is empty? Really?")
	#
	# 	print relation
	#
	# 	self.assertEqual(type(relation[1]), type([]), "Nested relations should appear as nested lists.")
	#

	# NEXT => create Relation as a category and use contents. Also: maintain ordinal info.
	# Need to verify that the Relation points to the items AND the items point to the relation.


	# def test_evaluate_atom(self):
	#
	# 	root = Category('*')
	#
	# 	parse_text = "foo"
	#
	# 	evaluate(0, tokenize(parse_text), root)
	#
	# 	self.assertEqual( len(root.contents), 1)
	#
	# 	self.assertTrue( "foo" in root.contents.keys() )
	#
	# 	self.assertTrue( isinstance( root.contents["foo"], Category) )
	#
	#
	# def test_evaluate_simple_expression(self):
	#
	# 	root = Category('*')
	#
	# 	parse_text = "2 + 3"
	#
	# 	evaluate(0, tokenize(parse_text), root)
	#
	# 	self.assertEqual( len(root.contents), 2)





if __name__ == '__main__':
    unittest.main()
