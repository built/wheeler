import unittest
from category import *
from category.stdout import *
from interpreter.tools import *

TRACK_TEST_CALLS = False

class TestCategoryOperation(unittest.TestCase):

	def test_create_category(self):
		foo = Category("foo")
		self.assertEqual("foo", foo.name)


	"""
	What should 'add' be capable of?
	You can add a Category or a list of Categories.
	Or any combination, like so:
	Category
	[Category, Category]
	[Category, [Category, Category], Category, Category]
	"""
	def test_add_category_to_category(self):
	
		root = Category('*')
	
		testcategory = Category('5', root)
	
		newcategory = Category("sub category!", root)
	
		testcategory.add(newcategory)
	
		category_names = [subcategory.name for subcategory in testcategory.contents.values()]
	
		self.assert_(newcategory.name in category_names, "Adding a category didn't work.")
	
	
	def test_remove_from_category(self):
	
		root = Category('*')
		root.associate("5", "meters")

		# We should see that the contents contains the category "meters"
		category_contents = [item.name for item in root.contents.values()]
	
		self.assert_("meters" in category_contents)
	
		root.disassociate('5', 'meters')
	
		# We should see that the contents contains the category "meters"
		five = root.comprehend('5')
		
		self.assert_('meters' not in five)
	
	# def test_create_anonymous_category(self):
	# 
	# 	root = Category('*')
	# 
	# 	self.assert_( root.create_anon().value == "relation_1")
	# 
	# 	self.assert_( root.create_anon().value == "relation_2")
	# 
	# 	root.create_anon()
	# 	root.create_anon()
	# 	root.create_anon()
	# 	root.create_anon()
	# 	root.create_anon()
	# 
	# 	self.assert_( root.create_anon().value == "relation_8")



if __name__ == '__main__':
    unittest.main()
