import unittest
import numpy as np

import assign

class ProbTests(unittest.TestCase):
	def test_prob_n(self):
		events = [0.5, 0.5, 0.5, 0.5, 0.5]
		res = assign.prob_n(events)

		np.testing.assert_allclose(res*2**5, [1, 5, 10, 10, 5, 1],
			err_msg="Equal propability events should be binomial")
		np.testing.assert_allclose(res.sum(), 1)

	def test_gauss_order(self):
		from scipy.stats import norm

		x1 = norm(10, 1)
		x2 = norm(10, 1)
		res = assign.prob_gauss_order(x1, x2, 10)
		np.testing.assert_allclose(res, 0.125,
			err_msg="A 45 degree slice from the center is wrong")

		res = assign.prob_gauss_order(x1, x2, 5)
		expected = 0.5 * (1 - x1.cdf(5)) * (1 - x2.cdf(5))
		np.testing.assert_allclose(res, expected,
			err_msg="A slice colinear with the center should match half the product")

if __name__ == '__main__':
	unittest.main()
