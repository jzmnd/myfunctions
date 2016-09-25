#! /usr/bin/env python
"""
myfunctions.py
My functions module comtaining commonly used functions

Created by Jeremy Smith on 2015-06-05
University of California, Berkeley
j-smith@ecs.berkeley.edu
Version 2.5

"""

import sys
import os
import numpy as np

from matplotlib.ticker import ScalarFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import FigureCanvasPdf
import seaborn
from scipy.signal import medfilt

__author__ = "Jeremy Smith"
__version__ = "2.5"


def adjAvSmooth(dataarray, N=10):
	"""Applies Median Filter then Smooths N Times with Adjacent Averaging and Fixed End-points"""
	lp = dataarray[-1]
	dataarray = medfilt(dataarray)
	dataarray[-1] = lp
	for i in range(N):
		dplus1 = np.roll(dataarray, 1)
		dplus1[0] = dplus1[1]
		dminus1 = np.roll(dataarray, -1)
		dminus1[-1] = dminus1[-2]
		dataarray = (dataarray + 0.5*dplus1 + 0.5*dminus1)/2.0
	return dataarray


def weibullPlot(dataarray):
	"""Calculates Weibull Plot Data from Input Array"""
	n = len(dataarray)
	datasorted = np.sort(abs(np.array(dataarray)))
	ecdf = []
	for i in range(n):
		ecdf.append(float(len(np.where(datasorted <= datasorted[i])[0]))/n)
	ecdf = np.array(ecdf)
	weibull = np.log(-np.log(1 - ecdf[:-1]))
	return np.log(datasorted)[:-1], weibull, datasorted, ecdf


def findNearest(arr, val):
	"""Finds Nearest Element in Array to val"""
	i = (np.abs(arr - val)).argmin()
	return i, arr[i]


def numDiff(y, x):
	"""Numerical Differentiation using Two-point Finite Difference"""
	grad = [0]
	for i, yi in enumerate(y[:-2]):
		g = (y[i+2] - yi)/(x[i+2] - x[i])
		grad.append(g)
	grad.append(0)
	return grad


def numDifference(y):
	"""Takes First Difference Between Adjacent Points"""
	diff = []
	for i, yi in enumerate(y[:-1]):
		d = y[i+1] - yi
		diff.append(d)
	diff.append(0)
	return diff


def numInt(function, a, b, step):
	"""Numerical Integration of a Function with x=a and x=b Limits"""
	x = np.array([float(x)*step for x in range(int(a/step), int(b/step)+1)])
	y = function(x)
	trpsum = 0
	for i, yi in enumerate(y[:-1]):
		trap = (x[i+1]-x[i])*(y[i+1]+yi)/2
		trpsum += trap
	return trpsum


def mean_sterr(x):
	"""Mean and Standard Error Function"""
	n, mean, std = len(x), 0, 0
	for a in x:
		mean = mean + a
	mean = mean/float(n)
	for a in x:
		std = std + (a - mean)**2
	std = np.sqrt(std/float(n - 1))
	return mean, std/np.sqrt(n)


def outputMultiList(data):
	"""Converts Single List of Output Data to Muliple Lists for Each VG"""
	dtnum = data["VGS"].count(data["VGS"][0])
	vds = data["VDS"][:dtnum]
	data2 = {"VDS": vds}
	for i in range(len(data["VGS"])/dtnum):
		data2["IDS" + str(i+1)] = data["IDS"][i*dtnum:(i+1)*dtnum]
	return data2


def paImport(datafile, path, ext_cut=6):
	"""Importer for Keithley PA Files"""
	device_name = datafile[:-ext_cut].strip()
	print device_name
	data = {}
	with open(os.path.join(path, datafile), 'r') as dfile:
		headers = dfile.readline().strip().split('\t')
		for h in headers:
			data[h] = []
		for line in dfile:
			splitline = line.strip().split('\t')
			if len(splitline) == 1:
				continue
			for i, a in enumerate(splitline):
				if "#REF" in a:
					a = 0
				data[headers[i]].append(float(a))
	return data, device_name


def paramImport(paramfile, path, param_no=3):
	"""Importer for Device Parameter File"""
	params = []
	for i in range(param_no):
		params.append({})
	with open(os.path.join(path, paramfile), 'r') as pfile:
		for line in pfile:
			splitline = line.strip().split('\t')
			name, values = splitline[0], splitline[1:]
			for i in range(param_no):
				params[i][name] = float(values[i])
	return params


def paImportLV(datafile, path, ext_cut=7):
	"""Importer for LabView Format Files"""
	device_name = datafile[:-ext_cut].strip()
	file_type = datafile[-ext_cut+1:-4].strip()
	if file_type == "oo":
		headers = ["VDS", "IDS", "VGS"]
	else:
		headers = ["VDS", "IDS", "VGS", "IGS"]
	data = {}
	for h in headers:
		data[h] = []
	with open(os.path.join(path, datafile), 'r') as dfile:
		dfile.readline()
		for line in dfile:
			splitline = line.strip().split("\t")
			if len(splitline) == 1:
				continue
			for i, a in enumerate(splitline):
				data[headers[i]].append(float(a))
	return data, device_name, file_type


def paImportImpSpec(datafile, path, ext_cut=9):
	"""Importer for Impedance Spec Format Files"""
	device_name = datafile[:-ext_cut].strip()
	file_type = datafile[-ext_cut+1:-4].strip()
	if file_type == "freq":
		headers = ["Freq", "ReZ", "ImZ", "T"]
	elif file_type == "bias":
		headers = ["Vbias", "ReZ", "ImZ", "T"]
	else:
		print "No File Type Tag"
		return
	data = {}
	for h in headers:
		data[h] = []
	with open(os.path.join(path, datafile), 'r') as dfile:
		for line in dfile:
			splitline = line.strip().split("\t")
			if len(splitline) == 1:
				continue
			if "NaN" in splitline:
				continue
			if float(splitline[2]) == 0:
				continue
			for i, a in enumerate(splitline):
				data[headers[i]].append(float(a))
	return data, device_name, file_type


def csvImport(datafile, path, headerlength):
	"""Importer for B1500 csv Files"""
	header = []
	data = {}
	with open(os.path.join(path, datafile), 'r') as dfile:
		for i in range(headerlength):
			splitline = dfile.readline().strip().split(',')
			header.append(splitline)
		colhead = dfile.readline().strip().split(',')    # Column headers
		for h in colhead:
			if h == '':
				continue
			data[h] = []
		for line in dfile:
			splitline = line.strip().split(',')
			if len(splitline) == 1:
				continue
			for i, a in enumerate(splitline):
				if a == '':
					continue
				data[colhead[i]].append(float(a))
	return data, header


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

			if datatype is None:
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


def dataOutput(filename, path, datalist, format="%.1f\t %e\t %e\t %e\n"):
	"""Writes Output to File in Results Folder"""
	formatlist = format.split(" ")
	if len(formatlist) != len(datalist):
		print "FORMAT ERROR"
		return
	if "results" not in os.listdir(path):
		os.mkdir(os.path.join(path, "results"))
	with open(os.path.join(path, "results", filename), 'w') as outfile:
		for i in range(len(datalist[0])):
			for cnum, c in enumerate(datalist):
				outfile.write(formatlist[cnum] %c[i])
	return


def dataOutputHead(filename, path, datalist, headerlist, format_d="%.1f\t %e\t %e\t %e\n", format_h="%s\n"):
	"""Writes Output to File in Results Folder and Includes Header"""
	formatlist_d = format_d.split(" ")
	formatlist_h = format_h.split(" ")
	if len(formatlist_d) != len(datalist):
		print "DATA FORMAT ERROR"
		return
	if len(formatlist_h) != len(headerlist):
		print "HEADER FORMAT ERROR"
		return
	if "results" not in os.listdir(path):
		os.mkdir(os.path.join(path, "results"))
	with open(os.path.join(path, "results", filename), 'w') as outfile:
		for i in range(len(headerlist[0])):
			for cnum, c in enumerate(headerlist):
				outfile.write(formatlist_h[cnum] %c[i])
		outfile.write('\n')
		for i in range(len(datalist[0])):
			for cnum, c in enumerate(datalist):
				outfile.write(formatlist_d[cnum] %c[i])
	return


def dataOutputGen(filename, path, datalist):
	"""Writes Output to File in Results Folder from 1D or 2D Arrays"""
	datalist = np.array(datalist)
	if len(datalist.shape) not in (1, 2):
		print "1D or 2D data array only"
		return
	if "results" not in os.listdir(path):
		os.mkdir(os.path.join(path, "results"))
	with open(os.path.join(path, "results", filename), 'w') as outfile:
		for row in datalist:
			if len(datalist.shape) == 1:
				outfile.write("{:s}\n".format(str(row)))
			else:
				for col in row:
					outfile.write("{:s}, ".format(str(col)))
				outfile.write('\n')
	return


def quickPlot(filename, path, datalist, xlabel="x", ylabel="y", xrange=["auto", "auto"], yrange=["auto", "auto"], yscale="linear", xscale="linear", col=["r", "b"]):
	"""Plots Data to .pdf File in Plots Folder Using matplotlib"""
	if "plots" not in os.listdir(path):
		os.mkdir(os.path.join(path, "plots"))
	coltab = col*10
	seaborn.set_context("notebook", rc={"lines.linewidth": 1.0})
	formatter = ScalarFormatter(useMathText=True)
	formatter.set_scientific(True)
	formatter.set_powerlimits((-2, 3))
	fig = Figure(figsize=(6, 6))
	ax = fig.add_subplot(111)
	for i, ydata in enumerate(datalist[1:]):
		ax.plot(datalist[0], ydata, c=coltab[i])
	ax.set_title(filename)
	ax.set_yscale(yscale)
	ax.set_xscale(xscale)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	if xrange[0] != "auto":
		ax.set_xlim(xmin=xrange[0])
	if xrange[1] != "auto":
		ax.set_xlim(xmax=xrange[1])
	if yrange[0] != "auto":
		ax.set_ylim(ymin=yrange[0])
	if yrange[1] != "auto":
		ax.set_ylim(ymax=yrange[1])
	if yscale == "linear":
		ax.yaxis.set_major_formatter(formatter)
	ax.xaxis.set_major_formatter(formatter)
	canvas = FigureCanvasPdf(fig)
	canvas.print_figure(os.path.join(path, "plots", filename+".pdf"))
	return
