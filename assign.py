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
    prob = np.zeros((colleges.shape[0] + 1,) + students.shape)

    # align the axes
    college_nums = np.arange(len(colleges))[:,np.newaxis]
    colleges = colleges[:,np.newaxis]


    # p_gi_lt_tk[k,i] = p(G_i + I_i < T_k)
    p_vi_lt_tk = norm(students.grade, sigma_i).cdf(colleges.threshold)

    # probability that one grade is beaten by another
    # p_gi_gt_gk[i,j] = P(G_i + I_i < G_j + I_j)
    #                 = P((G_i + I_i) - (G_j + I_j) < 0)
    # Note that the diagonal is zeros
    p_vi_lt_vj = norm(students[:,np.newaxis].grade - students.grade, np.sqrt(2) * sigma_i).cdf(0)
    np.fill_diagonal(p_vi_lt_vj, 0)

    print p_vi_lt_vj.round(2)

    # applied_mask[k,i] is true iff X_i == k
    applied_mask = students.choice == college_nums

    # rejection probability
    prob[-1,:] = np.sum(applied_mask*p_vi_lt_tk, axis=0) # sum over colleges

    # assume acceptance, for now
    prob[:-1][applied_mask] = 1 - p_vi_lt_tk[applied_mask]

    for ci, college in enumerate(colleges):
        #
        s_applied = students.choice == ci

        if np.sum(s_applied) <= college.capacity:
            # unconditionally accepted
            pass
        else:
            prob[ci,s_applied] *= np.nan
            # p_n_le_l[l] = P(count(s_applied))
            # p_n_le_l = np.cumsum(prob_n(p_gi_lt_tk[ci,s_applied]))
            # prob[ci,s_applied] *= p_n_le_l[college.capacity]


    return prob
