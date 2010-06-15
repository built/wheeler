def adder(categories):

	assert(isinstance(categories, list) and len(categories) > 0)

	# Since the entire interaction should be happening in a single
	# context, let's just use the context of the first item we see.
	context = categories[0].context

	numbers = [int(number.value) for number in categories]

	return context.create( str(sum( numbers )) )


def subtractor(categories):

	assert(isinstance(categories, list) and len(categories) > 0)

	# Since the entire interaction should be happening in a single
	# context, let's just use the context of the first item we see.
	context = categories[0].context
	
	# We should sort the categories by position first. No escaping position!

	numbers = [int(number.value) for number in categories]

	# Fugly - And apparently we don't get numbers in the order given.
	# Ah, we're pulling from contents, which is a hash.
	numbers = [numbers[0]] + [(-number) for number in numbers[1:]]
	
	print "Here's the list I will sum: %s" % numbers
	
	return context.create( str(sum( numbers )) )

	