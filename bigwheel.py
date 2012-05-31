#!/usr/bin/env python
from category import Category
import fileinput
import sys
from interpreter.tools import parse, evaluate, expand_arrows, has_dangling_quote
from common import *
import os

def load_file(filename):
	try:
		for line in open( os.path.dirname(os.path.abspath(__file__)) + "/%s.w" % filename, "r"):
			line = line.strip()
			# Comment stripper. Fragile!
			line = line[:line.find('#')] if '#' in line else line

			# Ignore blank lines
			if line:
				evaluate( parse( expand_arrows(line), ROOT), ROOT )
	except:
		print "Can't load that file for some damned reason or another."

def load_prelude():

	for line in open( os.path.dirname(os.path.abspath(__file__)) + "/prelude.w", "r"):
		line = line.strip()
		# Comment stripper. Fragile!
		line = line[:line.find('#')] if '#' in line else line

		# Ignore blank lines
		if line:
			evaluate( parse(line, ROOT), ROOT )

exiting = False

print "%s\nType 'exit', 'quit', or 'q' to quit." % VERSION

exit_commands = ('exit', 'quit', 'q')
clear_command = ('clear',)
help_command = ('help',)

help_text = """Commands:
	'exit', 'quit', or 'q' to end session
	'clear' to clear screen"""

load_prelude()

def next_line_of_input():
	line = raw_input(">> ") + "\n"
	if not has_dangling_quote(line): return line
	# Otherwise keep accumulating the line until we get balanced quotes.
	accumulating = True
	while(accumulating):
		nextline = raw_input() + "\n"
		line += nextline
		accumulating = not has_dangling_quote(nextline) # stop

	return line

while not exiting:

	line = next_line_of_input()

	command = line.lower().strip() # The line may be a REPL command.

	if command in exit_commands:
		exiting = True
		break

	if command in clear_command:
		import os
		os.system('clear' if sys.platform != 'win32' else 'cls')
		continue

	if command in ('help',):
		print help_text
		continue

	if command in ('reset',):
		ROOT = Category("*")
		ROOT.add(ROOT)
		load_prelude()
		print "* was reset"
		continue

	if command.split() and command.split()[0] == "load":
		args = command.split()
		if len(args) != 2:
			print "This didn't make sense for loading: ", args
		else:
			load_file(args[1])
		continue

	# Ignore blank lines
	if line:
		relations_before = len(ROOT.terms)
		evaluate( parse( expand_arrows(line), ROOT), ROOT )
		relations_after = len(ROOT.terms)












