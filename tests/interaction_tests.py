import unittest
from category import *
from category.stdout import *
from interpreter.tools import parse, evaluate

class TestInteractions(unittest.TestCase):

	def test_simple_interaction(self):

		root = Category('*')

		expression = "foo bar"

		evaluate(parse(expression, root), root)

		self.assertTrue( root.has("foo") )

		self.assertTrue( isinstance( root.contents["foo"], Category) )

		foo = root.contents["foo"]
		bar = root.contents["bar"]

		self.assertTrue(bar.related(set([foo])), "no double relation?")


	def test_another_interaction(self):

		root = Category('*')

		expression = "apple tasty red"

		evaluate(parse(expression, root), root)

		apple	= root.contents["apple"]
		tasty	= root.contents["tasty"]
		red		= root.contents["red"]

		# TODO: Make #related not suck.
		self.assertTrue(apple.related( set([tasty]) ), "no relation?")
		self.assertTrue(apple.related( set([red]) ), "no relation?")

		self.assertTrue(tasty.related( set([red]) ), "no relation?")
		self.assertTrue(tasty.related( set([apple]) ), "no relation?")

		self.assertTrue(red.related( set([tasty]) ) , "no relation?")
		self.assertTrue(red.related( set([apple]) ), "no relation?")


	def test_getting_a_thingy_between_two_other_thingies(self):

		root = Category('*')

		expression = "apple tasty red"

		evaluate(parse(expression, root), root)

		apple	= root.contents["apple"]
		tasty	= root.contents["tasty"]
		red		= root.contents["red"]

		related = root.comprehend("apple", "red")

		self.assertTrue(len(related) > 0, "We should have received some results back.")

		self.assertTrue( root.comprehend("apple", "red")[0].related( set([tasty]) ), "Can't find a relationship?")

	def test_getting_a_thingy_between_two_other_thingies2(self):

		root = Category('*')

		expression = "apple tasty red"

		evaluate(parse(expression, root), root)

		apple	= root.contents["apple"]
		tasty	= root.contents["tasty"]
		red		= root.contents["red"]

		relation = root.comprehend("apple", "red")

		self.assertTrue(len(relation) > 0, "We should have received some results back.")

		# TODO: Make this test less crude and more direct.
		self.assertTrue( tasty in relation[0].contents.values(), "Can't find a relationship?")



if __name__ == '__main__':
    unittest.main()
