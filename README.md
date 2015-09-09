#My Functions Module

Some useful functions by Jeremy Smith

Function List:
--------------

Math:  
`adjAvSmooth(dataarray, N=10)`  
`weibullPlot(dataarray)`  
`numInt(function, a, b, step)`  
`numDiff(y, x)`  
`numDifference(y)`  
`mean_sterr(x)  `  

Array manipulation:  
`findNearest(arr, val)`  
`outputMultiList(data)`  

File import:  
`paImport(datafile, path, ext_cut=6)`  
`paImportLV(datafile, path, ext_cut=7)`  
`paramImport(paramfile, path, param_no=3)`  
`paImportImpSpec(datafile, path, ext_cut=9)`  
`csvImport(datafile, path, headerlength)`  
`csvBiasStressImport(datafile, path)`  

File output:  
`dataOutput(filename, path, datalist, format="%.1f\t %e\t %e\t %e\n")`  
`dataOutputHead(filename, path, datalist, headerlist, format_d="%.1f\t %e\t %e\t %e\n", format_h="%s\n")`  
`dataOutputGen(filename, path, datalist)`  
`quickPlot(filename, path, datalist, xlabel="x", ylabel="y", xrange=["auto", "auto"], yrange=["auto", "auto"], yscale="linear", xscale="linear", col=["r","b"])`  

