import data
from scipy.stats import norm

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
