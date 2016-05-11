from scipy.stats import norm
import numpy as np
from data import Outcome

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

def prob_gauss_order(x2, x1, lim):
    """
    P(x2 > x1 > lim)
    http://math.stackexchange.com/q/1780335/1896
    """
    import scipy.integrate
    res, acc = scipy.integrate.quad(
        lambda x: x1.pdf(x) * (1 - x2.cdf(x)),
        a=lim,
        b=np.inf
    )
    return res



def prob_outcomes(colleges, students, sigma_i):
    """
    ret[si,outcome] = p(student has outcome o)
    """

    # set everything to 0
    prob = np.zeros(students.shape + (3,))

    # we can't make use of the vectorization inside norm in all cases, sadly
    student_dist_vec = norm(students.grade, sigma_i)
    student_dists = np.array([
        norm(s.grade, sigma_i) for s in students
    ])

    # align the axes
    college_nums = np.arange(len(colleges))[:,np.newaxis]
    colleges = colleges[:,np.newaxis]

    # p_gi_lt_tk[k,i] = p(G_i + I_i < T_k)
    p_vi_lt_tk = student_dist_vec.cdf(colleges.threshold)

    # applied_mask[k,i] is true iff X_i == k
    applied_mask = students.choice == college_nums

    # rejection probability
    prob[:,Outcome.REJECTED] = np.sum(applied_mask*p_vi_lt_tk, axis=0) # sum over colleges
    p_not_rejected = 1 - prob[:,Outcome.REJECTED]

    for ci, college in enumerate(colleges):        #
        s_applied = students.choice == ci

        if np.sum(s_applied) <= college.capacity:
            # unconditionally accepted
            prob[s_applied,Outcome.POOLED] = 0
            continue

        for si, student in enumerate(students):
            if not s_applied[si]:
                continue

            # mask for the other students who applied
            other_applied = s_applied.copy()
            other_applied[si] = False

            my_dist = student_dists[si]
            p_other_beat_me = np.array([
                prob_gauss_order(other_dist, my_dist, college.threshold) / p_not_rejected[si]
                for other_dist in student_dists[other_applied]
            ])

            p_at_least_l_beat_me = np.cumsum(prob_n(p_other_beat_me))

            print college.name, student.name, student.grade.round(2)
            for p_other, s_other in zip(p_other_beat_me, students[other_applied]):
                print "  ", p_other.round(2), s_other.grade.round(2)
            print

            prob[si, Outcome.POOLED] = p_at_least_l_beat_me[college.capacity] * p_not_rejected[si]

    prob[:,Outcome.ACCEPTED] = 1 - prob[:,Outcome.REJECTED] - prob[:,Outcome.POOLED]

    return prob

