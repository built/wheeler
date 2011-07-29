# Set up some things so that we can be sane.

# Print to stdout
transition (pattern print (string qualifier)) (action STDOUT)

# Let the interpreter and built-ins know that the interpreter is loaded.
prelude loaded
