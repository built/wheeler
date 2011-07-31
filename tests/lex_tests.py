import unittest
from interpreter.tools import *

TRACK_TEST_CALLS = True

class LexTests(unittest.TestCase):

	def test_tokenize_nothing(self):

		result = tokenize(None)

		self.assertEqual(result, [], "Tokenize should always return a list, even when given nothing.")

	def test_tokenize_atoms(self):

		expression = "foo bar 123 + 10 / 24 10/24/1954"

		self.assertEqual(tokenize(expression), ["foo", "bar", "123", "+", "10", "/", "24", "10/24/1954"])


	def test_tokenize_regexes(self):

		expression = r"/ABC\d+ZZZ[^c]/"

		self.assertEqual(tokenize(expression), [r"/ABC\d+ZZZ[^c]/"])


	def test_lex_atoms(self):

		expression = "foo - bar 123 + 10 / 24 10/24/1954"

		self.assertEqual(syntax_tree(expression), ["foo", "-", "bar", "123", "+", "10", "/", "24", "10/24/1954"])


	def test_tokenize_nested_expressions(self):

		expression = '15 "people!" (! to be confused with $10.00 or 10/10/10) (4 + 83 (0))'

		expected = ['15', '"people!"', '(', '!', 'to', 'be', 'confused', 'with', '$10.00', 'or', '10/10/10', ')', '(', '4', '+', '83', '(', '0', ')', ')']

		self.assertEqual(tokenize(expression), expected)


	def test_lex_nested_expressions(self):

		expression = '15 "people!" (! to be confused with $10.00 or 10/10/10) (4 + 83 (0))'

		expected = ['15', '"people!"', ['!', 'to', 'be', 'confused', 'with', '$10.00', 'or', '10/10/10'], ['4', '+', '83', ['0'] ]  ]

		self.assertEqual(syntax_tree(expression), expected)


	def test_lex_category_qualifiers_expressions(self):

		expression = '[string] "this is a zither"'

		expected = ['[string]', '"this is a zither"']

		self.assertEqual(syntax_tree(expression), expected)



if __name__ == '__main__':
    unittest.main()
