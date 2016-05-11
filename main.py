import data
import assign

colleges, students = data.test_data(others=6)

probs = assign.prob_outcomes(colleges, students, sigma_i=0.2)

print "Results:"
print
for ci, college in enumerate(colleges):
    print "{0.name} (T={0.threshold:.2f}, C={0.capacity})".format(college)
    for si, (student, p) in enumerate(zip(students, probs)):
        if student.choice != ci: continue
        print "  {0.name} (G={0.grade:.2f}):".format(student)
        for outcome in data.Outcome:
            print "    {:>8s}:{: 6.1f}".format(outcome.name, 100*p[outcome])
    print

