import numpy as np
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

num_arms = "25"
algorithm = ["epsilon-greedy", "UCB"]#, "KL-UCB", "Thompson-Sampling"]

pp = PdfPages('test.pdf')
pyplot.figure()
pyplot.clf()

for algo in algorithm:
    job_str = "client/report/arms_" + num_arms + "_" + algo + ".log"
    data = np.genfromtxt(job_str, delimiter=',')
    x = data[:, 0]
    y = data[:, 1]
    pyplot.plot(x, y, label=algo, lw=2)


pyplot.legend()
pyplot.xlabel('horizon (log scale)')
pyplot.ylabel('regret')
pyplot.xscale('log')
# pp.savefig()
# pp.close()
pyplot.show()
