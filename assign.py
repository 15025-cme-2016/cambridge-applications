def probabilities(colleges, students, sigma_i):
	"""
	Calculates the probability of a student ending up in a given college

	"""
	# raise NotImplementedError
	p = {}
	for college in colleges:
		for student in students:
			p[college, student] = float('nan')

	return p
