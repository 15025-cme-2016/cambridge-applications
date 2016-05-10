import data
from scipy.stats import norm
import numpy as np

def prob_n(event_probs):
    """
    Takes in the probability of a list of independant events
    Return p[i] = n(events) == i
    """
    # probability of an empty set of events is 1
    if len(event_probs) == 0:
        return np.array([1])

    # P(n(A,As...) == N) = P(a)P(n(As...) == N-1) + P(!a)P(n(As...) == N)
    first, rest = event_probs[0], event_probs[1:]

    res = np.zeros(len(event_probs) + 1)
    p_rest_n = prob_n(rest)
    res[1:] += first * p_rest_n
    res[:-1] += (1-first) * p_rest_n
    return res

def probabilities(colleges, students, sigma_i):
    """
    Calculates the probability of a student ending up in a given college

    """
    p = {}
    # set everything to 0
    for college in colleges:
        for student in students:
            p[college, student] = 0


    for college in colleges:
        applied = [s for s in students if s.choice == college]
        for student in students:
            # p(G + I < T)
            p_gi_lt_t = norm(student.grade, sigma_i).cdf(college.threshold)
            p[data.REJECTED, student] = p_gi_lt_t
            p[college, student] = float('nan')

    return p
