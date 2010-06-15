from category import Category
from category.stdout import *
from category.file import file
from category.math import *

VERSION = "Wheeler 0.0.5"

ROOT = Category("*")

# Set up some basic "types" in our context.
STRING = ROOT.create("string")
NUMBER = ROOT.create("number")
ANY = ROOT.create(".")

ROOT.create("+").add_handler(NUMBER, adder)
ROOT.create("-").add_handler(NUMBER, subtractor)

ROOT.create("print").add_handler( STRING, printer )
ROOT.create("println").add_handler( STRING, line_printer )

def dumper(category):
	file = open("dump.dot", "w")
	file.write("graph {\n")
	
	print "dumper called with %s" % type(category)
	if not islist(category):
		category.dump(file)
	else:
		for item in category:
			item.dump(file)

	file.write("}")
	file.close()

	return []
	

ROOT.create("dump").add_handler(ANY, dumper )


