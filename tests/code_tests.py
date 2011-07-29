import unittest
from category import *
from category.stdout import *
from interpreter.tools import *

TRACK_TEST_CALLS = False

class TestCategoryOperation(unittest.TestCase):

	def test_simplest_program(self):

		root = Category('*')

		# Define a transition that detects when something enters "foo". It should be connected to "bar"
		term = "works"
		evaluate(parse(term, root), root )

		transition = "foo -> bar"
		evaluate(parse(transition, root), root )

		matches = root.comprehend("bar", "works")

		expression = "foo works"
		evaluate(parse(expression, root), root )


	def test_external_code(self):
	
		root = Category('*')
		code_tag = root.create("code")
	
		transition = "code -> foo"
	
		evaluate(parse(transition, root), root )
	
		term = "code"
		evaluate(parse(term, root), root )


	# TO DO:
	# * Test transitions just with graphs to see if they will really fire like you think they will
	# * Wrap stdout and see if you can get something to print out
	# * Then try file I/O
	# * then try keyboard input. How will events be handled for input into a program? I bet it will involve a category...
	# * Put timestamps on everything


if __name__ == '__main__':
    unittest.main()










