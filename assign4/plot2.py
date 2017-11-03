import numpy as np

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('expt2.pdf')
pyplot.figure()
pyplot.clf()

fname = 'expt2_lmbda_{0}.out'
lmbda = ['0', '0.2', '0.4', '0.6', '0.8', '1']

for l in lmbda:
    print l
    with open(fname.format(l), 'r') as f:
        data = f.read().split('\n')[:-1]
    points = np.zeros([len(data), 2])
    for i, d in enumerate(data):
        points[i][0] = i + 1
        points[i][1] = np.mean([float(x) for x in d.split()])

    pyplot.plot(points[:, 0], points[:, 1], label="lambda = %s" % l)

pyplot.legend()
pyplot.xlabel('updates')
pyplot.ylabel('value function')
# pyplot.yscale('symlog')
pp.savefig()
pp.close()
# pyplot.show()
