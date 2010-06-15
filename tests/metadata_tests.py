import unittest
from category import *
from interpreter.tools import parse

class TestMetadata(unittest.TestCase):

	def test_has_metadata(self):

		expression = '"foo bar baz"'
		root = Category("*")
		result = parse(expression, root)

		self.assertTrue(result.has("metadata"), "All expressions should have metadata associated with them. This does not.")

		result.dump()
		
	def test_identify_string(self):

		expression = '"foo bar baz"'
		root = Category("*")
		result = parse(expression, root)

		self.assertTrue(result.has(expression))
		self.assertTrue(result.contents[expression].has("string"), "Expression is not picking up the intrinsic type.")

		# What we really want here is to have an intersection between our expression, metadata, and string.

		string_contents = root.contents["string"].contents.keys()

		metadata = result.contents["metadata"].contents.keys()


	def test_identify_numberic(self):

		expression = '123'
		root = Category("*")
		result = parse(expression, root)

		self.assertTrue(result.has(expression))
		self.assertTrue(result.contents[expression].has("number"), "Expression is not picking up the intrinsic type.")

	# def test_identify_expression(self):
	# 	self.fail("Nothing here yet")


if __name__ == '__main__':
    unittest.main()
