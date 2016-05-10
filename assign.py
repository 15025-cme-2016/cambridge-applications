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

    result[ci,si] = p(students[si] ends up at colleges[ci])
    result[-1,si] = p(students[si] is rejected)
    """
    # set everything to 0
    p = np.zeros((colleges.shape[0] + 1,) + students.shape)

    # align the axes
    colleges = colleges[:,np.newaxis]

    # p_gi_lt_tk[k,i] = p(G_i + I_i < T_k)
    p_gi_lt_tk = norm(students.grade, sigma_i).cdf(colleges.threshold)
    # chosen = students.choice == colleges

    # rejection probability
    p[-1,:] = p_gi_lt_tk[students.choice,np.arange(len(students))]

    return p
