import unittest
from category import *
from common import *
from category.test import *
from interpreter.tools import *

TRACK_TEST_CALLS = False

class TestReactions(unittest.TestCase):

	def test_simple_reaction(self):

		test = ROOT.create("test")

		test.add_handler( ANY, tester )

		transition_expression = "test 1"

		parse(transition_expression, ROOT).evaluate()

		self.assert_(len(ROOT.contents) > 0)

		self.assert_('TESTER_CALLED' in ROOT.contents)


if __name__ == '__main__':
    unittest.main()
