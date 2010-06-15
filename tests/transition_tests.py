import unittest
from category import *
from category.stdout import *
from interpreter.tools import *

TRACK_TEST_CALLS = False

class TestCategoryOperation(unittest.TestCase):

	def test_simple_transition(self):
	
		transition_expression = "baz when foo at bar"
		
		# evaluate
		# then look at root category that we passed in
		# Does that category look right?
		# Was a transition created?
		# Did the transition fire?
		# Test code: print "It works!" : "testing" @ test
		# > test "testing"
		# It works!
		# >
		root = Category()
		
		parse(transition_expression, root).evaluate() # Shouldn't eval happen in a context?

		self.assert_(len(root.contents) > 0)
		# 	
		# # For now let's use English words as delimiters. We were probably going to have to do
		# # this at some point anyway. ':' becomes 'when' and '@' becomes 'at'
		# # self.assert_('@' in root.contents, "'@' is an important token which should be visible")
		self.assert_('when' in root.contents)
		


		
if __name__ == '__main__':
    unittest.main()
