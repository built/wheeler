import random

GRAPHVIZ_RELATION = "[label=R, shape=circle, style=filled, fillcolor=cornflowerblue, fontcolor=white, color=navy]"
GRAPHVIZ_TRANSITION = "[label=Transition, fontsize=24, shape=diamond, style=filled, fillcolor=tomato, fontcolor=white, color=tomato4]"
GRAPHVIZ_ACTION = "[label=Action, fontsize=24, shape=diamond, style=filled, fillcolor=darkolivegreen3, fontcolor=white, color=darkolivegreen4]"
GRAPHVIZ_PATTERN = "[label=Pattern, fontsize=24, shape=diamond, style=filled, fillcolor=gold, fontcolor=black, color=gold3]"
GRAPHVIZ_CATEGORY = "[shape=box, style=filled, fillcolor=mediumpurple4, fontcolor=white, color=mediumpurple]"
GRAPHVIZ_CONTEXT = "[shape=doublecircle, style=filled, fillcolor=palegreen4, fontcolor=white, color=palegreen4]"
GRAPHVIZ_BUILTIN = "[shape=ellipse, style=filled, fillcolor=gray, fontcolor=black, color=mediumgray]"
BUILTINS = ['relation', 'transition', 'pattern', 'action', 'position', 'metadata', 'time']
GRAPHVIZ_ALT_CATEGORY = "[fontsize=36, fontname=Helvetica, shape=box, style=filled, fillcolor=lightslategray, fontcolor=white, color=lightslategray1]"


COLORS = "blue blue1 blue2 blue3 blue4 blueviolet brown brown1 brown2 brown3 brown4 burlywood burlywood1 burlywood2 burlywood3 burlywood4 cadetblue cadetblue1 cadetblue2 cadetblue3 cadetblue4 chartreuse chartreuse1 chartreuse2 chartreuse3 chartreuse4 chocolate chocolate1 chocolate2 chocolate3 chocolate4 coral coral1 coral2 coral3 coral4 cornflowerblue cornsilk3 cornsilk4 crimson darkgoldenrod darkgoldenrod1 darkgoldenrod2 darkgoldenrod3 darkgoldenrod4 darkgreen darkkhaki darkolivegreen darkolivegreen1 darkolivegreen2 darkolivegreen3 darkolivegreen4 darkorange darkorange1 darkorange2 darkorange3 darkorange4 darkorchid darkorchid1 darkorchid2 darkorchid3 darkorchid4 darksalmon darkseagreen darkseagreen1 darkseagreen2 darkseagreen3 darkseagreen4 darkslateblue darkslategray darkslategray3 darkslategray4 darkslategrey darkturquoise darkviolet deeppink deeppink1 deeppink2 deeppink3 deeppink4 deepskyblue deepskyblue1 deepskyblue2 deepskyblue3 deepskyblue4 dimgray dimgrey dodgerblue dodgerblue1 dodgerblue2 dodgerblue3 dodgerblue4 firebrick firebrick1 firebrick2 firebrick3 firebrick4".split()


def is_bracketed(name):
	return name.startswith("[") and name.endswith("]")

class CategoryInspector:

	def __init__(self, category):
		self.category = category
		self.already_dumped = []
		self.already_drawn = []

	def dump_to_file(self, filename):
		self.file = open(filename, "w")
		self.write("graph {\n")
		self.declare_category(self.category)
		self.dump(self.category)
		self.write("}\n")
		self.file.close()


	def dump_to_file_especial(self, filename):
		self.file = open(filename, "w")
		self.write("graph {\n")
		self.declare_category(self.category)
		self.dump_especial(self.category)
		self.write("}\n")
		self.file.close()

	def write(self, str):
		self.file.write(str)

	def dump(self, category):
		self.already_dumped += [category]

		for subcategory in category.contents.values():
			self.draw_connection(category, subcategory)
			if subcategory not in self.already_dumped:
				self.declare_category(subcategory)
				self.dump(subcategory)

	def dump_especial(self, category):
		self.already_dumped += [category]

		for subcategory in category.contents.values():
			if subcategory.name not in ["metadata", "position"] and len( set(["metadata", "position"]) & set(subcategory.contents.keys())) < 1:
				self.draw_connection(category, subcategory)
				if subcategory not in self.already_dumped:
					self.declare_category(subcategory)
					self.dump_especial(subcategory)

	def style(self, category):
		if category.name == "*": return GRAPHVIZ_CONTEXT
		if category.name in BUILTINS: return GRAPHVIZ_BUILTIN
		if is_bracketed(category.name): return GRAPHVIZ_ALT_CATEGORY
		if "transition" in category.contents:
			return GRAPHVIZ_TRANSITION
		elif "relation" in category.contents:
			return GRAPHVIZ_BUILTIN
		elif "action" in category.contents:
			return GRAPHVIZ_ACTION
		elif "pattern" in category.contents:
			return GRAPHVIZ_PATTERN
		elif "__relation__" not in category.name:
			return GRAPHVIZ_ALT_CATEGORY
		else:
			return GRAPHVIZ_RELATION

	def declare_category(self, category):
		self.write("%s%s;\n" % (self.safe_name(category.name), self.style(category)))

	def draw_connection(self, cat1, cat2):
		connection = tuple(sorted([cat1.name, cat2.name]))
		if connection not in self.already_drawn:
			self.already_drawn += [connection]
			self.write("%s--%s[color=%s];\n" % (self.safe_name(cat1.name), self.safe_name(cat2.name), random.choice(COLORS) ) )
		
	def safe_name(self, name):
		return '"%s"' % name if name in ['*', '+', '-', '.', '$_', '->'] or is_bracketed(name) else name

