import unittest
from category import *
from interpreter.tools import syntax_tree, parse, categorize, categorized_expression
from associative_tools import AssociativeSet

class TestCategoryInspector(unittest.TestCase):

	def test_generate_simple_dump(self):

		filename = "/nml/nextwheel/tests/test.dot"

		root = AssociativeSet('*')

		# parse_text = "foo bar (baz berz)"
		parse_text = "foo bar"

		parse(parse_text, root)

		# Expected: foo, bar, (baz berz), baz, berz, outer expression, inner expression (parenthetical)
		CategoryInspector(root).dump_to_file(filename)

		dumpfile = open(filename, "r")

		self.assertNotEqual(dumpfile, None, "Can't find the file?")

		content = dumpfile.readlines()

		self.assertTrue(len(content) > 0, "No lines read from dot file?")

		# We don't want duplicate relations. Let's only allow them once.
		# In this case our context is named '*' and our test category is 'bar'.
		lines_with_bar_and_star = [line for line in content if "bar" in line and "*" in line]

		self.assertTrue(len(lines_with_bar_and_star) == 1, "'bar' and '*' should appear only ONCE")

	# def test_exclude_context_if_asked(self):
	# 	omit = True
	# 	CategoryInspector(root, omit).dump_to_file(filename)
	# 	pass


if __name__ == '__main__':
    unittest.main()
