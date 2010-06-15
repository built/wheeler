#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
#!/usr/bin/env python
from category import Category
from category.stdout import printer
import fileinput
import re
import sys
from interpreter.tools import parse
from common import *

tokenized_lines = []

line_number = 1

for line in fileinput.input():

	line = line.strip()
	# Comment stripper. Fragile!
	line = line[:line.find('#')] if '#' in line else line

	# Ignore blank lines
	if line:
		parse(line, ROOT).evaluate()

