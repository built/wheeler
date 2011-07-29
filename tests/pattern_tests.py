import unittest
from category import *
from category.stdout import *
from interpreter.tools import *

class TestPatternMatching(unittest.TestCase):

	# -------------------------------------------------------
	# TEST LITERALS ALONE
	# -------------------------------------------------------

	def test_literal_single_match(self):
		root = Category('*')
		pattern = parse("pattern foo", root)
		expression =  parse("foo", root)

		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 1, "Should have ONE match only.")

		self.assertEqual(matches.pop().name, "foo")

	def test_literal_match_when_subset(self):
		root = Category('*')
		pattern = parse("pattern foo bar", root)
		expression =  parse("foo bar baz", root)

		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 2, "Should have TWO matches only. (foo and bar)")

	def test_literal_missing_match(self):
		root = Category('*')
		pattern = parse("pattern foo", root)
		expression =  parse("bar baz zither foof", root)

		self.assertFalse(match(root, pattern, expression), "Should have NO matches")

	def test_literal_partially_missing(self):
		root = Category('*')
		pattern = parse("pattern foo bar", root)
		expression =  parse("bar baz zither foof", root)

		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 0, "Should have NO matches")


	# -------------------------------------------------------
	# TEST QUALIFIEDS ALONE
	# -------------------------------------------------------
	def test_qualified_single_match(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)

		pattern = parse("pattern (AAA qualifier)", root)
		expression =  parse("foo", root)
		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 1, "Should have ONE match only.")

		self.assertEqual(matches.pop().name, "foo")


	# Multiple qualified
	def test_qualified_multiple_match(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)
		evaluate(parse("blarf bar", root), root)

		pattern = parse("pattern (AAA qualifier) (blarf qualifier)", root)
		expression =  parse("foo bar", root)
		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 2, "Should have two matching terms.")

		self.assertEqual(names(matches), set(["foo", "bar"]))

	# Qualified total mismatch
	def test_qualified_mismatch(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)
		evaluate(parse("blarf bar", root), root)

		pattern = parse("pattern (AAA qualifier) (blarf qualifier)", root)
		expression =  parse("fizz binn", root)
		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 0, "Nothing should have matched!")

	# Qualified partial (mis)match
	def test_qualified_partial_match(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)
		evaluate(parse("blarf bar", root), root)

		pattern = parse("pattern (AAA qualifier) (blarf qualifier)", root)
		expression =  parse("foo barney whoo hoo", root)
		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 0, "Nothing should match!")

	# -------------------------------------------------------
	# TEST LITERALS AND QUALIFIEDS TOGETHER
	# -------------------------------------------------------

	# Single literal, single qualified
	def test_mixed_match(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)

		pattern = parse("pattern bar (AAA qualifier)", root)
		expression =  parse("foo bar", root)
		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 2, "Should have two matching terms.")

		self.assertEqual(names(matches), set(["foo", "bar"]))

	def test_mixed_mismatch(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)

		pattern = parse("pattern bar (AAA qualifier)", root)
		expression =  parse("fizz bin bar", root)
		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 0, "Nothing should match!")

	# Gonzo! (More like Animal, really.)
	def test_mixed_craziness(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)
		evaluate(parse("blarf bar", root), root)

		pattern = parse("pattern ninja (AAA qualifier) assassin (blarf qualifier) woot", root)
		expression =  parse("woot jibberish foo spiffy ninja bar assassin and other things as well", root)
		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 5, "Should have FIVE matching terms.")

		self.assertEqual(names(matches), set("woot foo ninja bar assassin".split()))

	# -------------------------------------------------------
	# TEST FOR CYCLE CONDITIONS
	# -------------------------------------------------------

	# Qualified term can't be directly related to the expression
	# because it can cause an endless loop during evaluation.
	# def test_qualified_term_in_expression(self):
	# 	root = Category('*')
	# 	evaluate(parse("AAA foo", root), root)
	#
	# 	pattern = parse("pattern (AAA qualifier)", root)
	# 	qualified_term = root.comprehend("AAA", "qualifier")[0]
	# 	expression =  parse("some other stuff plus %s" % qualified_term.name, root)
	# 	matches = match(root, pattern, expression)
	#
	# 	self.assertTrue(qualified_term.name not in names(matches), "This will cause an endless loop during evaluation.")

	# # The expression term can't also be in the pattern terms or we'll get a cycle.
	# def test_expression_term_in_pattern(self):
	# 	root = Category('*')
	# 	evaluate(parse("AAA foo", root), root)
	#
	# 	pattern = parse("pattern flubber", root)
	# 	print pattern.terms
	# 	# qualified_term = root.comprehend("AAA", "qualifier")[0]
	# 	# expression =  parse("some other stuff plus", root)
	# 	# matches = match(root, pattern, expression)
	# 	#
	# 	# self.assertTrue(qualified_term.name not in names(matches), "This will cause an endless loop during evaluation.")


	# -------------------------------------------------------
	# "REAL WORLD" TESTS
	# -------------------------------------------------------

	# Display some stuff
	def test_mixed_match(self):
		root = Category('*')
		# evaluate(parse("foo string", root), root)

		pattern = parse("pattern print (string qualifier)", root)
		expression =  parse('print "foo"', root)
		matches = match(root, pattern, expression)

		self.assertEqual(len(matches), 2, "Should have two matching terms.")

		self.assertEqual(names(matches), set(["print", '"foo"']))




if __name__ == '__main__':
    unittest.main()
