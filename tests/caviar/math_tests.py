import unittest
from category import *
from common import *
from interpreter.tools import parse


class TestMath(unittest.TestCase):

	def test_simple_addition(self):
		expression = '1 + 2'

		result = parse(expression, ROOT).evaluate()

		self.assertTrue(result.has('3'), "Expected 3 in the result but I see: %s" % result.contents )


	def test_simple_subtraction(self):
		expression = '8 - 5'
		# self.fail("Subtraction doesn't work yet")
		result = parse(expression, ROOT).evaluate()

		self.assertTrue(result.has('3'), "Expected 3 in the result but I see: %s" % result.contents )


	def test_addition_of_sames(self):
		pass
		# expression = '1 + 1'
		#
		# root = Category("*")
		#
		# adder = root.create("+")
		#
		# expression_category = parse(expression, root)
		#
		# result = expression_category.evaluate()
		#
		# self.assertTrue(result.has('2'), "This language sucks at math! :) Expected 2." )




if __name__ == '__main__':
    unittest.main()
