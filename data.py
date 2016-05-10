""" Define some simple data_types"""
from collections import namedtuple

Student = namedtuple('Student', 'name grade choice')
College = namedtuple('College', 'name value capacity threshold')

def test_data():
	"""
	Generate some test data

	returns a tuple of colleges, students
	"""
	import random
	THRESH = 0.5

	# define some colleges
	caius    = College(name='Caius',    value=10, capacity=1, threshold=THRESH)
	queens   = College(name='Queens',   value=8,  capacity=3, threshold=THRESH)
	homerton = College(name='Homerton', value=5,  capacity=2, threshold=THRESH)
	colleges = [caius, queens, homerton]

	# and some students, most of which are just random samples
	students = [
		Student(name='Eric', grade=0.8, choice=caius),
		Student(name='Tom', grade=0.9, choice=queens),
		Student(name='Alex', grade=0.7, choice=queens),
		Student(name='Ruifan', grade=0.7, choice=homerton) #about the same distance away
	] + [
		Student(name='Anon {}'.format(i), grade=random.random(), choice=random.choice(colleges))
		for i in range(6)
	]

	return colleges, students
