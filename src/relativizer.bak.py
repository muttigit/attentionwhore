#!/usr/bin/env python

import svg_parser2
import math as m
finalPath = []
finalPathScaled = []

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def relativize(svgPaths):
	global finalPath 
	global finalPathScaled 
	
	svgPaths.reverse()

	""" MUST DO:
		Relativize maximum to 18 units!
		x=0 at X=-0.09 in cartesian frame
		y=0 at Y=-0.322 in cartesian frame

		Read first two pops as width / height

		For now it's fixed
	"""
	maxVal = 297.039
	scalFactor = 0.177 / maxVal

	print 'scalFactor: ' + str(scalFactor)
	
	for path in finalPath:
		tmpPath = []
		for coord in path:
			coordTmp = coord
			if isFloat(coord):
				coordTmp = float(coord) * scalFactor
			tmpPath.append(coordTmp)
		finalPathScaled.append(tmpPath)

	#print 'finalPathScaled:'
	#print finalPathScaled

	#finalPathScaled = [float(coord)**scalFactor for path in finalPath for coord in path if isFloat(coord)]

	""" Check syntax
	    and do stuff
	"""
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

			simplePath = ['m']

			nextItem = svgPaths[len(svgPaths)-1]

			while(isFloat(nextItem)):
				x = float(svgPaths.pop()) + float(prevX)
				y = float(svgPaths.pop()) + float(prevY)
				simplePath.append(x)
				simplePath.append(y)
				prevX = x
				prevY = y
				nextItem = svgPaths[len(svgPaths)-1]

			finalPath.append(simplePath)
			
			print simplePath

		elif pathType == 'C':
			simplePath = ['C']

			nextItem = svgPaths[len(svgPaths)-1]

			while(isFloat(nextItem)):
				x = float(svgPaths.pop())
				y = float(svgPaths.pop())
				simplePath.append(x)
				simplePath.append(y)
				nextItem = svgPaths[len(svgPaths)-1]
			
			finalPath.append(simplePath)
			
			print simplePath

		elif pathType == 'c':
			prevX = finalPath[len(finalPath) - 1][1]
			prevY = finalPath[len(finalPath) - 1][2]

			simplePath = ['c']

			nextItem = svgPaths[len(svgPaths)-1]

			while(isFloat(nextItem)):
				x = float(svgPaths.pop()) + float(prevX)
				y = float(svgPaths.pop()) + float(prevY)
				prevX = x
				prevY = y
				simplePath.append(x)
				simplePath.append(y)
				nextItem = svgPaths[len(svgPaths)-1]
			
			finalPath.append(simplePath)

			print simplePath
		elif pathType == 'Z':
			simplePath = ['Z', startX ,startY]
			
			finalPath.append(simplePath)
			
			print simplePath

		elif pathType == 'l':
			prevX = finalPath[len(finalPath) - 1][1] 
			prevY = finalPath[len(finalPath) - 1][2]

			simplePath = ['l']

			nextItem = svgPaths[len(svgPaths)-1]

			while(isFloat(nextItem)):
				x = float(svgPaths.pop()) + float(prevX)
				y = float(svgPaths.pop()) + float(prevY)
				prevX = x
				prevY = y
				simplePath.append(x)
				simplePath.append(y)
				nextItem = svgPaths[len(svgPaths)-1]

			finalPath.append(simplePath)
			
			print simplePath		
	
	""" MUST DO:
		Fernandize all movements/coordinates
	"""
	#xCoords = []
	#yCoords = []
	#for path in finalPath:
	#	for x in range(1, len(path), 2):
	#		xCoords.append(path[x])
	#		yCoords.append(path[x+1])
		

def binomialCoefficient(n, k):
	return (m.fak(n)/(m.fak(k)*m.fak(n-k)))

def sumBezierElement(n, i, t, pointList):
	B = binomialCoefficient(n,i) * m.pow(1-t,n-i) * m.pow(t,i) * pointList[i-1][0]

	return B + sumBezierElement(n, i+1, t, pointList)

if __name__ == '__main__':
	listOfPaths = svg_parser2.getListOfPaths()
	for x in listOfPaths:
		relativize(x)

	print "The Final Path is: " + str(finalPath)	
	print "The Final Path Scaled is: " + str(finalPathScaled)	




