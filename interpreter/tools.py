# Parsing/interpreting tools for the runtime and interpreter.
import re
from time import time, strftime
from itertools import *
from category import Category, CategoryInspector
from associative_tools import AssociativeSet

LABEL, VALUE = 0, 1

def iscategory(obj):
	return isinstance(obj, Category)

def islist(obj):
	return type(obj) == type([])

def isstr(obj):
	return isinstance(obj, str)

parens = r"\(|\)"
bare_phrase = r"[\w|\=|\||\.|\*|\+|\-|\/|\!|\$|\<|\>\[\]]+"
quoted_phrase = r"\"[^\"]*\""
regex_phrase = r"/[^\/\s]*\/"
TOKENS = re.compile( "|".join([regex_phrase, quoted_phrase, parens, bare_phrase]) )

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

def parse(expression, context=None):
	categorized_expression = categorize( syntax_tree(expression) , context)
	annotate(context)
	return categorized_expression

def annotate(context):
	string, number, regex, metadata = create_tags(context, "string", "number", "regex", "metadata")

	for item in context.contents.values():
		if re.match(quoted_phrase, item.name):
			interact(context, item, string, metadata)
		elif re.match(r"\d+", item.name):
			interact(context, item, number, metadata)
		elif re.match(regex_phrase, item.name):
			interact(context, item, regex, metadata)


def categorized_expression(new_categories, context):
	expression = interact(context, *new_categories)
	position, metadata = create_tags(context, "position", "metadata")

	# Enumerate each term's original position in the originating expression.
	i = 0
	for category in new_categories:
		number = context.lookup_items_by_name(str(i))[0]
		context.add(number)
		interact(context, category, expression, metadata, position, number)
		i += 1

	return expression

def categorize(tokenized_expression, context):
	tokenized_expression = [categorize(item, context) if islist(item) else item for item in tokenized_expression]
	new_categories = convert_all_to_categories(tokenized_expression, context)
	return categorized_expression(new_categories, context)

def convert_all_to_categories(tokenized_expression, context):
	# Now we're guaranteed a flat list, some of which are Categories. Let's make them all categories now.
	for i in range(len(tokenized_expression)):
		if not iscategory(tokenized_expression[i]):
			tokenized_expression[i] = create_category(tokenized_expression[i], context)

	return tokenized_expression

def create_category(token, context):
	if not isstr(token): return token # I think this is really "ensure is category"
	return context.contents[token] if token in context.contents else Category(token, context)

def create_tags(context, *tagnames):
	tags = [context.lookup_items_by_name(tagname)[0] for tagname in tagnames]
	for tag in tags:
		context.connect(tag)
	return tags

def is_qualifier(category):
	return "qualifier" in category.contents

def is_regex(context, category):
	return [term for term in context.comprehend(category.name, "regex", "metadata") if term.name != context.name]

def is_relation(category):
	return "__relation__" in category.name

def is_negated(category):
	return "not" in category.contents

def pattern_terms(context, pattern):
	return [term for term in pattern.contents.values()
		if term.name != context.name
		and term.name != "pattern"
		and ( (is_qualifier(term) or is_negated(term)) or not is_relation(term) ) ]

def negated_terms(context, negated):
	return [term for term in negated.contents.values()
		if term.name != context.name
		and term.name != "not"] if is_negated(negated) else []

def quality(context, qualifier):
	return [term for term in qualifier.contents.values() if term.name != context.name and term.name != "qualifier" and not is_relation(term)]

def no_relations(names):
	return [name for name in names if "__relation__" not in name]

def pure_terms(terms, *exclude):
	return no_relations([term for term in terms.terms if term not in exclude])

def action(context, transition):
	actions = context.comprehend("action", "!metadata", transition.name)
	if actions:
		return actions[0]
	return None # This pains me. Falling through with null. TODO: Grace.

def pattern(context, transition):
	patterns = context.comprehend("pattern", "!metadata", transition.name)
	if patterns:
		return patterns[0]
	return None # This pains me. Falling through with null. TODO: Grace.

def dump_pattern(context, pattern):
	print "-= PATTERN DUMP =-"

	for term in pattern:
		if is_qualifier(term):
			qualified = qualified_type(context, term)

			print "[%s]" % (qualified if qualified else 'EVERYTHING')
		else:
			print term.name

	print "-= ------------ =-"

def qualified_type(context, term):
	types = quality(context, term)
	return types[0].name if types else '' # Default to no type, aka "everything".

def match(context, transition, expression):
	pure_pattern = pattern_terms(context, pattern(context, transition))
	expression_terms = [term for term in expression.contents.values() if term.name != context.name and "metadata" not in term.terms]
	action_terms = set(no_relations(action(context, transition).terms)) - set([context.name, "action"])
	literals = {term.name:None for term in pure_pattern if not is_qualifier(term) and not is_negated(term) and not is_regex(context, term)}

	regexes = {term.name:None for term in pure_pattern if is_regex(context, term)}

	qualifieds = {term:[] for term in pure_pattern if is_qualifier(term)}

	negateds = {x for x in names(list(chain.from_iterable([negated_terms(context, term) for term in pure_pattern if is_negated(term)]))) if "__relation__" not in x}

	negateds = negateds | action_terms

	negated_found = False

	for expression_term in expression_terms:
		for literal_term in literals.keys():
			if literal_term == expression_term.name:
				literals[literal_term] = expression_term

		if expression_term.name in negateds:
			negated_found = True
			break

		for regex_term in regexes.keys():
			if re.match(regex_term[1:-1], expression_term.name):
				regexes[regex_term] = expression_term

		for qualified_term in qualifieds.keys():
			qualifying_set = set(term for term in qualified_term.contents.values() if term.name != context.name and "__relation__" not in term.name and term.name != "qualifier")
			qualification = [expression_term.name] + list(names(qualifying_set))
			relationship = [relation for relation in context.comprehend(*qualification) if relation.name != context.name]
			if relationship and expression_term.name not in qualified_term.terms:
				qualifieds[qualified_term] += [expression_term]

	# Don't return nulls, only real matches.
	all_matches = [match for match in literals.values() if match] + [match for match in regexes.values() if match] + list(chain.from_iterable(match for match in qualifieds.values() if match))

	# ALL terms in the pattern must have a match.
	return all_matches if all(literals.values()) and all(qualifieds.values()) and all(regexes.values()) and not negated_found else []


def interact(context, *categories):
	if not categories: return context
	interaction = context.create_relation() # Worry about the vanity names option later.
	attach_timestamp(context, interaction)
	for category in categories:
		interaction.connect(category)
		context.connect(category)  # TODO: Why is this needed? Tests break w/o it, but why?
	return interaction

def evaluate(expression, context):
	expressions = []

	for transition in all_transitions(context):
		matches = match(context, transition, expression)
		if matches:
			if action(context, transition):
				pattern_terms = set(pure_terms(pattern(context, transition), 'pattern'))
				action_terms = set(pure_terms(action(context, transition), 'action'))
				parameters = {m.name for m in matches} - pattern_terms
				expressions += [ " ".join(action_terms | parameters) ]

	for new_expression_string in expressions:
		evaluate( parse(new_expression_string, context), context)

	if expression:
		if "dump" in expression.terms:
			dump(context, expression.terms)
			return
		elif "STDOUT" in expression.terms:
			if context.comprehend("prelude", "loaded"):
				printout(context, expression)
				return


def shorthand(name):
	return name.replace("__relation__", "R")

def dump(context, categories):
	for category in categories:
		subcategory_names = [shorthand(name) for name in category.terms if name != context.name]
		if subcategory_names:
			print "%s {%s}" % (shorthand(category.name), ", ".join(subcategory_names) )


def destring(string):
	return string[1:-1] if re.match(quoted_phrase, string) else string

def printout(context, categories):
	print "".join([destring(c) for c in categories.terms if c not in ['STDOUT', '*'] and "__relation__" not in c])


def attach_timestamp(context, interaction):
	timestamp = context.create_relation()
	for tag in create_tags(context, "metadata", "time"):
		timestamp.connect(tag)

	time_labels = create_tags(context, "year", "month", "date", "hour", "minute", "second")
	time_values = create_tags(context, *strftime("%Y %m %d %H %M %S").split())

	for time in zip(time_labels, time_values):
		time_component = context.create_relation()
		time_component.connect(time[LABEL])
		time_component.connect(time[VALUE])
		time_component.connect(timestamp)

	timestamp.connect(interaction)

def names(categories):
	return set([cat.name for cat in categories])

def all_transitions(context):
	return [transition for transition in context.comprehend("transition", "!metadata") if "metadata" not in transition.terms]


