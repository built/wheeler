import unittest
from category import *
from interpreter.tools import *

class TestPatternMatching(unittest.TestCase):

	# -------------------------------------------------------
	# TEST LITERALS ALONE
	# -------------------------------------------------------

	def test_literal_single_match(self):
		root = Category('*')
		transition = parse("transition (pattern foo) (action no_action)", root)
		expression =  parse("foo", root)

		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 1, "Should have ONE match only.")

		self.assertEqual(matches.pop().name, "foo")

	def test_literal_match_when_subset(self):
		root = Category('*')
		transition = parse("transition (pattern foo bar) (action no_action)", root)
		expression =  parse("foo bar baz", root)

		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 2, "Should have TWO matches only. (foo and bar)")

	def test_literal_missing_match(self):
		root = Category('*')
		transition = parse("transition (pattern foo) (action no_action)", root)
		expression =  parse("bar baz zither foof", root)

		self.assertFalse(match(root, transition, expression), "Should have NO matches")

	def test_literal_partially_missing(self):
		root = Category('*')
		transition = parse("transition (pattern foo bar) (action no_action)", root)
		expression =  parse("bar baz zither foof", root)

		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 0, "Should have NO matches")


	# -------------------------------------------------------
	# TEST QUALIFIEDS ALONE
	# -------------------------------------------------------
	def test_qualified_single_match(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)

		transition = parse("transition (pattern (AAA)) (action no_action)", root)
		expression =  parse("foo", root)
		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 1, "Should have one match, and ONE match only.")

		self.assertEqual(matches.pop().name, "foo")


	# Multiple qualified
	def test_qualified_multiple_match(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)
		evaluate(parse("blarf bar", root), root)

		transition = parse("transition (pattern (AAA) (blarf)) (action no_action)", root)
		expression =  parse("foo bar", root)
		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 2, "Should have two matching terms.")

		self.assertEqual(names(matches), set(["foo", "bar"]))

	# Qualified total mismatch
	def test_qualified_mismatch(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)
		evaluate(parse("blarf bar", root), root)

		transition = parse("transition (pattern (AAA) (blarf)) (action no_action)", root)
		expression =  parse("fizz binn", root)
		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 0, "Nothing should have matched!")

	# Qualified partial (mis)match
	def test_qualified_partial_match(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)
		evaluate(parse("blarf bar", root), root)

		transition = parse("transition (pattern (AAA) (blarf))  (action no_action)", root)
		expression =  parse("foo barney whoo hoo", root)
		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 0, "Nothing should match!")

	# -------------------------------------------------------
	# TEST LITERALS AND QUALIFIEDS TOGETHER
	# -------------------------------------------------------

	# Single literal, single qualified
	def test_mixed_match(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)

		transition = parse("transition (pattern bar (AAA)) (action no_action)", root)
		expression =  parse("foo bar", root)
		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 2, "Should have two matching terms.")

		self.assertEqual(names(matches), set(["foo", "bar"]))

	def test_mixed_mismatch(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)

		transition = parse("transition (pattern bar (AAA)) (action no_action)", root)
		expression =  parse("fizz bin bar", root)
		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 0, "Nothing should match!")

	# Gonzo! (More like Animal, really.)
	def test_mixed_craziness(self):
		root = Category('*')
		evaluate(parse("AAA foo", root), root)
		evaluate(parse("blarf bar", root), root)

		transition = parse("transition (pattern ninja (AAA) assassin (blarf) woot) (action no_action)", root)
		expression =  parse("woot jibberish foo spiffy ninja bar assassin and other things as well", root)
		matches = match(root, transition, expression)

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
	# 	transition = parse("transition (pattern (AAA qualifier)", root)
	# 	qualified_term = root.comprehend("AAA", "qualifier")[0]
	# 	expression =  parse("some other stuff plus %s" % qualified_term.name, root)
	# 	matches = match(root, transition, expression)
	#
	# 	self.assertTrue(qualified_term.name not in names(matches), "This will cause an endless loop during evaluation.")

	# # The expression term can't also be in the pattern terms or we'll get a cycle.
	# def test_expression_term_in_pattern(self):
	# 	root = Category('*')
	# 	evaluate(parse("AAA foo", root), root)
	#
	# 	transition = parse("transition (pattern flubber", root)
	# 	print pattern.terms
	# 	# qualified_term = root.comprehend("AAA", "qualifier")[0]
	# 	# expression =  parse("some other stuff plus", root)
	# 	# matches = match(root, transition, expression)
	# 	#
	# 	# self.assertTrue(qualified_term.name not in names(matches), "This will cause an endless loop during evaluation.")


	# -------------------------------------------------------
	# "REAL WORLD" TESTS
	# -------------------------------------------------------

	# Display some stuff
	def test_mixed_match(self):
		root = Category('*')
		# evaluate(parse("foo string", root), root)

		transition = parse("transition (pattern print (string)) (action no_action)", root)
		expression =  parse('print "foo"', root)
		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 2, "Should have two matching terms.")

		self.assertEqual(names(matches), set(["print", '"foo"']))


	# -------------------------------------------------------
	# TEST REGEXES ALONE
	# -------------------------------------------------------
	def test_regex_single_match(self):
		root = Category('*')

		transition = parse(r"transition (pattern /A\d+B\d+C/) (action no_action)", root)
		expression =  parse("foo", root)
		matches = match(root, transition, expression)

		self.assertFalse(matches, "Nothing should match yet.")

		expression =  parse("A123B456C", root)
		matches = match(root, transition, expression)

		self.assertEqual(len(matches), 1, "Should have a match.")

		self.assertEqual(matches.pop().name, "A123B456C")

	# # -------------------------------------------------------
	# # TEST NEGATIONS
	# # -------------------------------------------------------
	# # TODO: Decide in full how negations will work.
	# def test_negated_single_match(self):
	# 	root = Category('*')
	#
	# 	transition = parse(r"transition (pattern (not foo))", root)
	# 	expression =  parse("foo", root)
	# 	matches = match(root, transition, expression)
	#
	# 	self.assertFalse(matches, "Nothing should match yet.")
	#
	# 	expression =  parse("bar", root)
	# 	matches = match(root, transition, expression)
	#
	# 	print "Matches:"
	# 	print matches
	#
	# 	self.assertEqual(len(matches), 1, "Should have a match.")
	#
	# 	self.assertEqual(matches.pop().name, "bar")



if __name__ == '__main__':
    unittest.main()
