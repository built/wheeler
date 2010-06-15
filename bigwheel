#!/usr/bin/env python
from category import Category
from category.stdout import printer
import fileinput
import re
import sys
from interpreter.tools import parse
from common import *

exiting = False

print "%s\nType 'exit' to quit." % VERSION

exit_commands = ('exit', 'quit', 'q')
clear_command = ('clear',)
help_command = ('help',)

while not exiting:

	line = raw_input(">> ").strip()
	command = line.lower() # The line may be a REPL command.
	
	if command in exit_commands:
		exiting = True
		break

	if command in clear_command:
		import os
		os.system('clear' if sys.platform != 'win32' else 'cls')
		continue

	if command in ('help',):
		print """Type 'exit' or 'quit' to end session or 'clear' to clear screen"""
		continue
	
	# Ignore blank lines
	if line:
		result = parse(line, ROOT).evaluate()
		if result.contents.keys():
			print result.contents.keys()[0]












