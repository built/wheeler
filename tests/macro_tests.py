import unittest
from interpreter.tools import expand_arrows

class TestCategoryOperation(unittest.TestCase):

	def test_transition_expansion(self):
		test_line = "foo -> bar"
		self.assertEqual("transition (pattern foo) (action bar)", expand_arrows(test_line))


if __name__ == '__main__':
    unittest.main()
