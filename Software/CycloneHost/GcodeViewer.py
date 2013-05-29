#!/usr/bin/python

# AUTHOR:
#   Carlosgs (http://carlosgs.es)
# LICENSE:
#   Attribution - Share Alike - Creative Commons (http://creativecommons.org/licenses/by-sa/3.0/)
#
# DISCLAIMER:
#   This software is provided "as is", and you use the software at your own risk. Under no
#   circumstances shall Carlosgs be liable for direct, indirect, special, incidental, or
#   consequential damages resulting from the use, misuse, or inability to use this software,
#   even if Carlosgs has been advised of the possibility of such damages.

# Begin modules
import sys

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

import GcodeParser as gcp
# End modules

def plotPoints(path_list, color, linewidth): # Thanks to pprzemek (http://stackoverflow.com/questions/2282727/draw-points-using-matplotlib-pyplot-x1-y1-x2-y2)
	for path in path_list :
		a = np.array(path) # Give to plot() the points in the adequate format
		line, = plt.plot(a[:,0], a[:,1], color, linewidth=linewidth*3)
		#line.set_antialiased(False) # turn off antialising

def plotPath(etch_moves, travel_moves, etch_color, travel_color, etch_diam, travel_diam):
	plotPoints(etch_moves, etch_color, etch_diam)
	plotPoints(travel_moves, travel_color, travel_diam)

def view(filePath,fileName):
	
	#filePath = "../GcodeGenerators/pyGerber2Gcode_CUI/out/"
	#fileName = "printshield" # sys.argv[1]
	
	plt.figure()
	
	drill_diam = 0.8
	etch_diam = 0.1
	etch2pass_diam = 0.5
	etch3pass_diam = 1
	edge_diam = 2.4
	travel_diam = etch_diam
	
	#	b: blue
	#	g: green
	#	r: red
	#	c: cyan
	#	m: magenta
	#	y: yellow
	#	k: black
	#	w: white
	
	drill_color = 'r'
	etch_color = '#00DF00'
	etch2pass_color = '#50EF00'
	etch3pass_color =  '#A0FF00'
	edge_color = 'b'
	travel_color = 'c'
	
	plt.hold(True)
	plt.title("Gcode viewer")
	plt.axis('equal') # 1:1 aspect ratio
	
	print "\n Loading etch..."
	gcode_file = filePath+fileName+"_etch.gcode"
	(etch_moves, travel_moves, gcode_originXY, grid_sizeXY) = gcp.parseGcodeRaw(gcode_file)
	(etch_moves, travel_moves) = gcp.optimize(etch_moves)
	plotPath(etch_moves, travel_moves, etch_color, travel_color, etch_diam, travel_diam)
	
	print "\n Loading etch (2nd pass)..."
	gcode_file = filePath+fileName+"_etch2pass.gcode"
	(etch_moves, travel_moves, gcode_originXY, grid_sizeXY) = gcp.parseGcodeRaw(gcode_file)
	(etch_moves, travel_moves) = gcp.optimize(etch_moves)
	plotPath(etch_moves, travel_moves, etch2pass_color, travel_color, etch2pass_diam, travel_diam)
	
	print "\n Loading etch (3nd pass)..."
	gcode_file = filePath+fileName+"_etch3pass.gcode"
	(etch_moves, travel_moves, gcode_originXY, grid_sizeXY) = gcp.parseGcodeRaw(gcode_file)
	(etch_moves, travel_moves) = gcp.optimize(etch_moves)
	plotPath(etch_moves, travel_moves, etch3pass_color, travel_color, etch3pass_diam, travel_diam)
	
	print "\n Loading drill..."
	gcode_file = filePath+fileName+"_drill.gcode"
	(etch_moves, travel_moves, gcode_originXY, grid_sizeXY) = gcp.parseGcodeRaw(gcode_file)
	(etch_moves, travel_moves) = gcp.optimize(etch_moves)
	plotPath(etch_moves, travel_moves, drill_color, travel_color, drill_diam, travel_diam)
	
	print "\n Loading edge..."
	gcode_file = filePath+fileName+"_edge.gcode"
	(etch_moves, travel_moves, gcode_originXY, grid_sizeXY) = gcp.parseGcodeRaw(gcode_file)
	(etch_moves, travel_moves) = gcp.optimize(etch_moves)
	plotPath(etch_moves, travel_moves, edge_color, travel_color, edge_diam, travel_diam)
	
	plt.ion() # Enable real-time plotting to avoid blocking behaviour for pyplot
	plt.show()
	
	return plt
