#!/usr/bin/env python

import svg_parser2
finalPath = []

def relativize(svgPaths):
	global finalPath 
	
	"""	Read and push coordinates
		Read first two pops as width / height

		For now it's fixed
	"""

	maxVal = 297.039
	scalFactor = 0.18 / maxVal

	print 'scalFactor: ' + str(scalFactor)
	
	svgPaths.reverse()
	while(len(svgPaths) != 0):
		x = 0
		y = 0
		prevX = 0
		prevY = 0
		simplePath = []
		
		pathType = svgPaths.pop()
		if pathType =='': 
			print "ZERO CHAR REMOVED"

		elif pathType == 'M':
			x = svgPaths.pop()
			y = svgPaths.pop()

			startX = x
			startY = y

			simplePath = ['M', x, y]
			
			finalPath.append(simplePath)
			
			print simplePath

		elif pathType == 'm':
			prevX = finalPath[len(finalPath) - 1][1]
			prevY = finalPath[len(finalPath) - 1][2]

			x = svgPaths.pop()
			y = svgPaths.pop()

			print 'prevX: ' + prevX
			print 'prevY: ' + prevY

			print 'x: ' + x
			print 'y: ' + y

			simplePath = ['m', x, y]
			
			finalPath.append(simplePath)
			
			print simplePath

		elif pathType == 'C':
			#Bezier Curve Poles
			x1 = svgPaths.pop()
			y1 = svgPaths.pop()
			x2 = svgPaths.pop()
			y2 = svgPaths.pop()
			#Target Point
			x = svgPaths.pop()
			y = svgPaths.pop()
			
			simplePath = ['C', x1, y1, x2, y2, x, y]
			
			finalPath.append(simplePath)
			
			print simplePath

		elif pathType == 'c':
			prevX = finalPath[len(finalPath) - 1][1]
			prevY = finalPath[len(finalPath) - 1][2]
			
			#Bezier Curve Poles
			x1 = svgPaths.pop() + prevX
			y1 = svgPaths.pop() + prevY
			x2 = svgPaths.pop() + prevX
			y2 = svgPaths.pop() + prevY
			#Target Point
			x = svgPaths.pop() + prevX
			y = svgPaths.pop() + prevY
			
			simplePath = ['c', x1, y1, x2, y2, x, y]
			
			finalPath.append(simplePath)

			print simplePath
		elif pathType == 'Z':
			simplePath = ['Z',startX ,startY]
			
			finalPath.append(simplePath)
			
			print simplePath

		elif pathType == 'l':
			prevX = finalPath[len(finalPath) - 1][1] 
			prevY = finalPath[len(finalPath) - 1][2]

			x = svgPaths.pop() + prevX
			y = svgPaths.pop() + prevY

			simplePath = ['l', x, y]
			
			finalPath.append(simplePath)
			
			
			print simplePath		
		#else:
			#print "FIRST ELEMENT WAS:"+ str(pathType)+"\n SOMETHING WENT WRONG !\nBEWARE WILL PUSH ON LIST ANYWAY !!!!!\n DIRTY DIRTY FIX !!!!"	
			#finalPath[len(finalPath)-1].append(pathType)
	""" MUST DO:
		Relativize maximum to 18 units!
		x=0 at X=-0.09 in cartesian frame
		y=0 at Y=-0.322 in cartesian frame
	"""
	
	""" MUST DO:
		Fernandize all movements/coordinates
	"""
	
if __name__ == '__main__':
	
	""" main """
	listOfPaths = svg_parser2.getListOfPaths()
	for x in listOfPaths:
		zList=listOfPaths
		print zList[0]
		relativize(x)
	print "The Final PAth is: "+str(finalPath)	
