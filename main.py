import data
import assign

colleges, students = data.test_data()

probs = assign.probabilities(colleges, students, sigma_i=0.2)

print "Results:"
print
for student in students:
    print "{}:".format(student.name)
    total_prob = sum(probs[college, student] for college in colleges)
    for college in colleges:
        print "  {:>10s}:{: 6.1f}".format(college.name, 100*probs[college, student])
    print "  {:>10s}:{: 6.1f}".format('Rejected', (1 - total_prob) * 100)
