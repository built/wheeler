import unittest
import re
from category import *
from interpreter.tools import parse, no_relations

year_pattern = r"^\d{4,4}$"
month_pattern = r"^\d{1,2}$"
date_pattern = r"^\d{1,2}$"
hour_pattern = r"^\d{1,2}$"
minute_pattern = r"^\d{2,2}$"
second_pattern = r"^\d{2,2}$"

def extract_time_component(matches, label):
	return (set(no_relations(matches[0].contents.keys())) - set([label, "*"])).pop()

class TestMetadata(unittest.TestCase):

	def test_has_metadata(self):

		expression = '"foo bar baz"'
		root = Category("*")
		result = parse(expression, root)
		metadata = root.contents["metadata"]

		self.assertTrue(result.related( set([metadata]) ), "All expressions should have metadata associated with them. This does not.")

	def test_identify_string(self):

		expression = '"foo bar baz"'
		root = Category("*")
		parse(expression, root)

		match = root.comprehend(expression, "string", "metadata")

		self.assertTrue(len(match) > 0, "Not seeing string metadata for this expression.")


	# # For future version! Strings should be more normal.
	# def test_identify_string(self):
	#
	# 	expression = '"foo bar baz"'
	#
	# 	print "Syntax tree:"
	# 	print syntax_tree(expression)
	#
	# 	root = Category("*")
	# 	parse(expression, root)
	#
	# 	match = root.comprehend(expression, "string", "metadata")
	#
	# 	self.assertFalse(match, "Shouldn't retain the quotes!")
	#
	# 	match = root.comprehend(expression[1:-1], "string", "metadata") # Trim off the quotes.
	#
	# 	self.assertTrue(match, "Not seeing string metadata for this expression.")


	def test_identify_numeric(self):

		expression = '123'
		root = Category("*")
		result = parse(expression, root)

		match = root.comprehend(expression, "number", "metadata")

		self.assertTrue(len(match) > 0, "Not seeing 'number' metadata for this expression.")

	def test_timestamp(self):

		expression = '123'
		root = Category("*")
		result = parse(expression, root)
		time_match = root.comprehend(result.name, "time", "metadata")
		self.assertTrue(len(time_match) > 0, "Not seeing 'time' metadata for this expression.")

		timestamp = time_match[0]

		# YEAR
		#-----------------------------------------------------------------------
		match = root.comprehend(timestamp.name, "year")
		self.assertTrue(len(match) > 0, "Not seeing 'year' info.")
		year = extract_time_component(match, "year")
		self.assertTrue(re.match(year_pattern, year), "Not seeing year value.")

		# MONTH
		#-----------------------------------------------------------------------
		match = root.comprehend(timestamp.name, "month")
		self.assertTrue(len(match) > 0, "Not seeing 'month' info.")
		month = extract_time_component(match, "month")
		self.assertTrue(re.match(month_pattern, month), "Not seeing month value.")

		# DATE
		#-----------------------------------------------------------------------
		match = root.comprehend(timestamp.name, "date")
		self.assertTrue(len(match) > 0, "Not seeing 'date' info.")
		date = extract_time_component(match, "date")
		self.assertTrue(re.match(date_pattern, date), "Not seeing date value.")

		# HOUR - Go with 24 hour clock for now.
		#-----------------------------------------------------------------------
		match = root.comprehend(timestamp.name, "hour")
		self.assertTrue(len(match) > 0, "Not seeing 'hour' info.")
		hour = extract_time_component(match, "hour")
		self.assertTrue(re.match(hour_pattern, hour), "Not seeing hour value.")

		# MINUTE
		#-----------------------------------------------------------------------
		match = root.comprehend(timestamp.name, "minute")
		self.assertTrue(len(match) > 0, "Not seeing 'minute' info.")
		minute = extract_time_component(match, "minute")
		self.assertTrue(re.match(minute_pattern, minute), "Not seeing minute value.")

		# SECOND
		#-----------------------------------------------------------------------
		match = root.comprehend(timestamp.name, "second")
		self.assertTrue(len(match) > 0, "Not seeing 'second' info.")
		second = extract_time_component(match, "second")
		self.assertTrue(re.match(second_pattern, second), "Not seeing second value.")


if __name__ == '__main__':
    unittest.main()
