import data
import assign
import itertools
import numpy as np

colleges, students = data.test_data(others=60)

NDIM = 3

result = np.zeros((len(colleges),)*NDIM + (NDIM,))

for choices in itertools.product(np.arange(len(colleges)), repeat=NDIM):
    students.choice[:NDIM] = choices

    print "C:", choices

    probs = assign.prob_outcomes(colleges, students, sigma_i=0.2)

    print "Results:"
    print
    for ci, college in enumerate(colleges):
        print "{0.name} (T={0.threshold:.2f}, C={0.capacity})".format(college)
        for si, (student, p) in enumerate(zip(students[:NDIM], probs)):
            if student.choice != ci: continue
            print "  {0.name} (G={0.grade:.2f}):".format(student)
            for outcome in data.Outcome:
                print "    {:>8s}:{: 6.1f}".format(outcome.name, 100*p[outcome])
        print


    prob_c = assign.prob_colleges(colleges, students, probs)

    e_payoff = np.sum(prob_c * np.append(colleges.value, 0)[:,np.newaxis],axis=0)

    result[choices + (np.s_[:],)] = e_payoff[:NDIM]
    if False:
        print '{:>10s}{}'.format(
            '',
            ' '.join([
                "{:>10s}".format(college.name)
                for college in colleges
            ] + [
                "{:>10s}".format("Rejected")
            ])
        )
        for si, student in enumerate(students[:NDIM]):
            print "{:>10s}{}".format(
                student.name,
                ' '.join(
                    "{:10.2f}".format(p*100)
                    for p in prob_c[:,si]
                )
            )

np.save('result.npy', result)