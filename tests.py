import unittest
import numpy as np

import assign

class ProbTests(unittest.TestCase):
	def test_prob_n(self):
		events = [0.5, 0.5, 0.5, 0.5, 0.5]
		res = assign.prob_n(events)

		np.testing.assert_allclose(res*2**5, [1, 5, 10, 10, 5, 1])
		np.testing.assert_allclose(res.sum(), 1)

if __name__ == '__main__':
	unittest.main()
