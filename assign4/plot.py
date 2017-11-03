import argparse
import numpy as np

from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('expt1.pdf')
pyplot.figure()
pyplot.clf()

parser = argparse.ArgumentParser()
parser.add_argument('-file', '--file', type=str, default='expt1.out', help='IP of server')

args = parser.parse_args()

with open(args.file, 'r') as f:
    data = f.read().split('\n')[:-1]

points = np.zeros([len(data), 7])

for i, d in enumerate(data):
    points[i][0] = i + 1
    points[i][1:] = np.array([float(x) for x in d.split()])


for i in range(1, 7):
    pyplot.plot(points[:, 0], points[:, i], label="State %s" % i)

pyplot.legend()
pyplot.xlabel('updates')
pyplot.ylabel('value function')
pyplot.yscale('symlog')
pp.savefig()
pp.close()
# pyplot.show()
