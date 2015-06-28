import sys
import os
import numpy as np

from matplotlib.ticker import ScalarFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import FigureCanvasPdf
from scipy.signal import medfilt


def weibullPlot(dataarray):
	"""Calculates Weibull Plot Data from Input Array"""
	n = len(dataarray)
	datasorted = np.sort(abs(np.array(dataarray)))
	ecdf = []
	for i in range(n):
		ecdf.append(float(len(np.where(datasorted <= datasorted[i])[0]))/n)
	ecdf = np.array(ecdf)
	weibull = np.log(-np.log(1 - ecdf[:-1]))
	return np.log(datasorted), weibull

#print weibullPlot([1.7, 1.95, 2.5, 2.9, 4, 4.15, 4.4, 4.75, 4.9, 4.9, 5])[0]
#print weibullPlot([1.7, 1.95, 2.5, 2.9, 4, 4.15, 4.4, 4.75, 4.9, 4.9, 5])[1]

def csvBiasStressImport(datafile, path):
	"""Importer for Bias Stress Test csv Files from EasyExpert"""

	datalist_transfer = []
	datalist_stress = []
	data_transfer = {}
	data_stress = {}
	datatype = None

	with open(os.path.join(path, datafile), 'r') as dfile:
		for line in dfile:
			splitline = line.strip().split(', ')

			if splitline[0] == 'SetupTitle':
				if splitline[1] == 'I/V-t Sampling':
					datatype = 1
				elif splitline[1] == 'I/V Sweep':
					datatype = 2
				else:
					datatype = None
					continue

			if datatype == None:
				continue

			if splitline[0] == 'DataName':
				headerlist = splitline[1:]
				if datatype == 1:
					datalist_stress.append(data_stress)
					data_stress = {}
					for h in headerlist:
						data_stress[h] = []
				if datatype == 2:
					datalist_transfer.append(data_transfer)
					data_transfer = {}
					for h in headerlist:
						data_transfer[h] = []

			if splitline[0] == 'DataValue':
				if datatype == 1:
					for i, a in enumerate(splitline[1:]):
						data_stress[headerlist[i]].append(float(a))
				if datatype == 2:
					for i, a in enumerate(splitline[1:]):
						data_transfer[headerlist[i]].append(float(a))

		datalist_stress.append(data_stress)
		datalist_transfer.append(data_transfer)

	return datalist_transfer[:0:-1], datalist_stress[:0:-1]


path = os.path.dirname(os.path.abspath(__file__))

b, c = csvBiasStressImport("Bias Stress 4V LIN [ITO_5-1_pbs_01(2) ; 6_16_2015 6_02_56 PM].csv", path)

print b[7]

