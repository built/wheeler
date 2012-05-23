#!/usr/bin/env python
from category import Category
import fileinput
import sys
from interpreter.tools import parse, evaluate, expand_arrows
from common import *
import os

def load_prelude():

	for line in open(os.path.dirname(os.path.abspath(__file__)) + "/prelude.w", "r"):
		line = line.strip()
		# Comment stripper. Fragile!
		line = line[:line.find('#')] if '#' in line else line

		# Ignore blank lines
		if line:
			evaluate( parse( expand_arrows(line), ROOT), ROOT )

load_prelude()

tokenized_lines = []

line_number = 1

for line in fileinput.input():

	line = line.strip()
	# Comment stripper. Fragile!
	line = line[:line.find('#')] if '#' in line else line

	# Ignore blank lines
	if line:
		evaluate( parse(line, ROOT), ROOT )
