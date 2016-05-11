""" Define some simple data_types"""
from collections import namedtuple
import numpy as np
from enum import IntEnum

class Outcome(IntEnum):
    REJECTED = 0
    POOLED = 1
    ACCEPTED = 2

# this would be the more pythonic way:
Student = namedtuple('Student', 'name grade choice')
College = namedtuple('College', 'name value capacity threshold')

# But we should use numpy for efficiency
college_dtype = np.dtype((np.record, [
    ('name', np.str_, 24),
    ('value', np.float64),
    ('capacity', np.uint16),
    ('threshold', np.float64)
]))
student_dtype = np.dtype((np.record, [
    ('name', np.str_, 24),
    ('grade', np.float64),
    ('choice', np.intp)
]))

REJECTED = -1

def test_data(others=6):
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
    colleges = np.rec.fromrecords([caius, queens, homerton], dtype=college_dtype)


    Student(name='Eric', grade=0.8, choice=caius)

    # and some students, most of which are just random samples
    students = np.rec.fromrecords([
        Student(name='Eric', grade=0.8, choice=0),
        Student(name='Perfect', grade=1, choice=0),
        Student(name='Tom', grade=0.9, choice=1),
        Student(name='Alex', grade=0.7, choice=1),
        Student(name='Ruifan', grade=0.7, choice=2) #about the same distance away
    ] + [
        Student(
            name='Anon {}'.format(i),
            grade=random.random(),
            choice=np.random.randint(len(colleges)))
        for i in range(others)
    ], dtype=student_dtype)

    return colleges, students
