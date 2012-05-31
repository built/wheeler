import unittest
from interpreter.tools import expand_arrows, has_dangling_quote

class TestCategoryOperation(unittest.TestCase):

	def test_transition_expansion(self):
		test_line = "foo -> bar"
		self.assertEqual("transition (pattern foo) (action bar)", expand_arrows(test_line))

	def test_quote_imbalance(self):
		"""
		For instance, if there is a line with three quote characters, it probably needs to 
		be considered multi-line. Or there is a typo.
		"""
		test_line = '"foo" -> "bar '
		self.assertTrue( has_dangling_quote(test_line))

if __name__ == '__main__':
    unittest.main()
