import unittest
from category import *
from common import *
from interpreter.tools import parse

class TestPrecedence(unittest.TestCase):

	def test_categories_receive_precedence(self):

		plus = ROOT.contents["+"]
		precedence = ROOT.contents["precedence"]
		three = ROOT.contents["3"]
		
		self.assertTrue("+" in ROOT.contents, "'+' isn't defined?")
		
		self.assertTrue(three in plus.intersection(precedence), "Addition hasn't the right precedence.")
		
		expression = '1 + 2'
		
		expression_category = parse(expression, ROOT)

		self.assertTrue("precedence" in expression_category.contents["+"].contents, "No precedence found for '+'!")
		
		self.assertTrue("+" in expression_category.contents["+"].contents["precedence"].contents, "Precedence category doesn't know about '+'?")


	def test_arithmetic_precedence(self):

		expression = '1 + 2 / 5 * 3 - 2'

		expression_category = parse(expression, ROOT)

		metadata = expression_category.contents["metadata"]
		plus = expression_category.contents["+"]
		minus = expression_category.contents["-"]
		mult = expression_category.contents["*"]
		div = expression_category.contents["/"]
		
		operators = (plus, minus, mult, div)
		
		precedence = ROOT.contents["precedence"]
		
		self.assertTrue("0" in [category.name for category in precedence.intersection(div)], "Division should have precedence zero")
		self.assertTrue("1" in [category.name for category in precedence.intersection(mult)], "Multiplication should have precedence one")
		self.assertTrue("2" in [category.name for category in precedence.intersection(minus)], "Subtraction should have precedence two")
		self.assertTrue("3" in [category.name for category in precedence.intersection(plus)], "Addition should have precedence three")



if __name__ == '__main__':
    unittest.main()
