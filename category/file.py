from category import *

file = Category("file")

def set_filename(category):

	# TODO: Fix this!
	print "set filename to %s" % category.value


file.add_handler( Category("RENAME_ME"), set_filename )


# We want to take action when unified with 

# This will be used like so: file "foo"

# To actually read from the file, the category will need to be passed an output stream



