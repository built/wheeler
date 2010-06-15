# Parsing/interpreting tools for the runtime and interpreter.
import re
from category import Category, ContainingModuleNameGivenInsteadOfClassName, iscategory

def islist(obj):
	return type(obj) == type([])


parens = r"\(|\)"
bare_phrase = r"[\w|\=|\||\.|\*|\+|\-|\/|\!|\$]+"
quoted_phrase = r"\"[^\"]*\""

TOKENS = re.compile( "|".join([parens, bare_phrase, quoted_phrase]) )


def unbalanced_parens(string):
	parens_difference = 0

	for char in string:
		if char == '(':
			parens_difference += 1
		elif char == ')':
			parens_difference -= 1

	return (parens_difference != 0)

def tokenize(expression):
	return [] if not expression else [token for token in re.findall(TOKENS, expression)]


EXPRESSION_START = '('
EXPRESSION_END = ')'

def lex(stream):
	"""
	Convert a stream of tokens into an expression tree.
	"""
	tree = []
	branch_history = [tree]
	current_branch = branch_history[0]

	for token in stream:

		if token == EXPRESSION_START:
			new_branch = []
			branch_history.append(new_branch)
			current_branch.append(new_branch)
			current_branch = new_branch

		elif token == EXPRESSION_END:
			#move back to the original branch.
			branch_history.pop()
			current_branch = branch_history[-1]

		else:
			current_branch.append(token)

	return tree

def syntax_tree(expression):
	return lex( tokenize(expression) )

def parse(expression, given_context=None):
	return categorize( syntax_tree(expression) , given_context)

def rebuild_expression(nested_token_list):
	"""
	We need the full expression so we can properly name certain categories.
	What better way to do that than to recreate them from the parse tree instead
	of just hanging on to the original expression?
	Glad you're coming with me on that.
	"""
	expression = ""
	first_field = True # until we deal with the first!
	for token in nested_token_list:
		if islist(token):
			expression += " " + rebuild_expression(token)
		else:
			expression += ("%s" % token) if first_field else (" %s" % token)
			first_field = False

	return "(%s)" % expression.strip()

def find_or_create_outer_category(tokenized_expression, given_context):
	if rebuild_expression(tokenized_expression) not in given_context.contents:
		return Category(rebuild_expression(tokenized_expression), given_context)
	else:
		return given_context.contents[rebuild_expression(tokenized_expression)]

def categorize(tokenized_expression, given_context):

	containing_category = find_or_create_outer_category(tokenized_expression, given_context)

	# Sometimes this is a list. Can't initialize a Category with a list.
	# Let's prescan to handle list situations and emit a category for those.
	tokenized_expression = [categorize(item, given_context) if islist(item) else item for item in tokenized_expression]

	# Now we're guaranteed a flat list, some of which are Categories. Let's make them all categories now.
	tokenized_expression = convert_all_to_categories(tokenized_expression, given_context)

	# Now we're guaranteed a flat list of Categories. Add them into the return envelope.
	containing_category.add(tokenized_expression)

	containing_category.create("metadata")

	return containing_category


def convert_all_to_categories(tokenized_expression, given_context):
	# Now we're guaranteed a flat list, some of which are Categories. Let's make them all categories now.
	for i in range(len(tokenized_expression)):
		if not iscategory(tokenized_expression[i]):
			tokenized_expression[i] = create_classified_category(tokenized_expression[i], given_context)

	return tokenized_expression

def create_classified_category(token, given_context):

	if token in given_context.contents:
		return given_context.contents[token]

	category = Category(token, given_context)
	if re.match(quoted_phrase, category.value):
		category.add(Category("string", given_context) if "string" not in given_context.contents else given_context.contents["string"])
	elif re.match(r"^\d+$", category.value):
		category.add(Category("number", given_context) if "number" not in given_context.contents else given_context.contents["number"])

	return category


def evaluate(line_number, line, root):
	"""Here we're expected a line number from the source file, the 'line' as a list of tokens, and the 'root'
	or parent category space."""

	# Ensure everything passed to us is represented as a category.
	categories = [ Category(token) if token not in root.contents else root.contents[token] for token in line ]

	# TODO: Remove the following once it is no longer needed for debugging purposes.
	if str( type(categories[0]) ) == "<type 'module'>":
		raise ContainingModuleNameGivenInsteadOfClassName

	# Put any new categories into the root category.
	for cat in categories:
		if cat.name not in root.contents:
			root.contents[cat.name] = cat

	interaction_results = []

	# Add all given categories to each other.
	for this_category in categories:
		others = [other for other in categories if other is not this_category]
		if others:
			interaction_results += [this_category.add(others)]

	return Category(interaction_results)

def create_relation(tokens, root):
	"""Here we're expecting a list of tokens, and the 'root'
	or parent category space. We're going to emit a list of categories.
	BUT we will not evaluate them."""

	# Ensure everything passed to us is represented as a category.
	categories = [ Category(token) if token not in root.contents else root.contents[token] for token in tokens ]

	# Add any new categories to the root category we've been given. Note that
	# while we don't want RELATIONS to be evaluated yet (and their categories to interact)
	# we still need to track new categories when they are created.

	# Put any new categories into the root category.
	for cat in categories:
		if cat.name not in root.contents:
			root.add(cat)

	return categories


def typedump(msg, items):
	print "typedump:"
	print msg
	for item in items:
		print type(item)
	print "---"

def valdump(msg, items):
	print "valdump:"
	print msg
	for item in items:
		print item
	print "---"





