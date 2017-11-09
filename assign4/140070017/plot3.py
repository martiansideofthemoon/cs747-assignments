import ast
import numpy as np

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('expt1_2.pdf')
pyplot.figure()
pyplot.clf()

weights = ['w[%d]' % i for i in range(1, 8)]

with open('weights.txt', 'r') as f:
    data = f.read().split('\n')[:-1]

data = [ast.literal_eval(x) for x in data]
data = np.array(data)

for i, d in enumerate(weights):
    pyplot.plot(np.arange(len(data)), data[:, i], label=d)

pyplot.legend()
pyplot.xlabel('updates')
pyplot.ylabel('parameter value')
pyplot.yscale('symlog')
pp.savefig()
pp.close()
# pyplot.show()
