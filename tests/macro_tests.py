import unittest

def expand_arrows(line):
	if '->' not in line: return line

	# Only consider two-part transitions for now.
	(front, back) = [x.strip() for x in line.split('->')][:2]

	return "transition (pattern %s) (action %s)" % (front, back)

class TestCategoryOperation(unittest.TestCase):


	def test_transition_expansion(self):
		test_line = "foo -> bar"
		
		self.assertEqual("transition (pattern foo) (action bar)", expand_arrows(test_line))



if __name__ == '__main__':
    unittest.main()
