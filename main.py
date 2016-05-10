import data
import assign

colleges, students = data.test_data()

probs = assign.probabilities(colleges, students, sigma_i=0.2)

print "Results:"
print
for student in students:
    print "{}:".format(student.name)
    for college in colleges:
        print "  {:>10s}:{: 6.1f}".format(college.name, 100*probs[college, student])
    print "  {:>10s}:{: 6.1f}".format('Rejected', 100*probs[data.REJECTED, student])
