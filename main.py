import data
import assign

colleges, students = data.test_data()

probs = assign.probabilities(colleges, students, sigma_i=0.2)

print "Results:"
print
for si, student in enumerate(students):
    print "{} (G={:.2f}):".format(student.name, student.grade)
    for ci, college in enumerate(colleges):
        print "  {:>10s}:{: 6.1f}".format(college.name, 100*probs[ci, si])
    print "  {:>10s}:{: 6.1f}".format('Rejected', 100*probs[data.REJECTED, si])
