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
	svgPathsScaled = []
	simplePath = []
	
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
	
	#svgPathsScaled = [(float(coord)*scalFactor) for coord in svgPaths if coord == isFloat(coord)]
	for coord in svgPaths:
		coordTmp = coord
		if isFloat(coord):
			coordTmp = float(coord) * scalFactor
			svgPathsScaled.append(coordTmp)
		else:
			svgPathsScaled.append(coord)
	
	svgPathsScaled.reverse()
	
	print 'svgPathsScaled:'
	print svgPathsScaled

	""" Check syntax
	    and do stuff
	"""
	while(len(svgPathsScaled) != 0):
		x = 0
		y = 0
		prevX = 0
		prevY = 0
		
		pathType = svgPathsScaled.pop()
		if pathType =='': 
			print "ZERO CHAR REMOVED"

		elif pathType == 'M':
			print 'M'
			if (len(simplePath) != 0):
				finalPath.append(simplePath)
			simplePath = []

			x = svgPathsScaled.pop()
			y = svgPathsScaled.pop()

			startX = x
			startY = y

			simplePath.append(x)
			simplePath.append(y)
			
			print 'simplePathAfter-M'
			print simplePath
			
		elif pathType == 'm':
			finalPath.append(simplePath)
			simplePath = []

			prevX = finalPath[len(finalPath) - 1][len(finalPath[len(finalPath) - 1]) - 1]
			prevY = finalPath[len(finalPath) - 1][len(finalPath[len(finalPath) - 1]) - 1]

			nextItem = svgPathsScaled[len(svgPathsScaled)-1]

			while(isFloat(nextItem)):
				x = float(svgPathsScaled.pop()) + float(prevX)
				y = float(svgPathsScaled.pop()) + float(prevY)
				simplePath.append(x)
				simplePath.append(y)
				prevX = x
				prevY = y
				nextItem = svgPathsScaled[len(svgPathsScaled)-1]

		elif pathType == 'C':
			prevX = simplePathScaled[len(simplePath)-2]
			prevY = simplePathScaled[len(simplePath)-1]

			bezierCoordsX = []
			bezierCoordsY = []

			nextItem = svgPathsScaled[len(svgPathsScaled)-1]

			while(isFloat(nextItem)):
				x = float(svgPathsScaled.pop())
				y = float(svgPathsScaled.pop())

				simplePath.append(x)
				simplePath.append(y)
				nextItem = svgPathsScaled[len(svgPathsScaled)-1]
		
			for t in range(0, 360-1):
				xBezier = sumBezierElement(len(bezierCoordsX), 0, (1/360)*t, bezierCoordsX)
				yBezier = sumBezierElement(len(bezierCoordsY), 0, (1/360)*t, bezierCoordsY)
				simplePath.append(xBezier)
				simplePath.append(yBezier)

		elif pathType == 'c':
			prevX = simplePath[len(simplePath)-2]
			prevY = simplePath[len(simplePath)-1]

			bezierCoordsX = []
			bezierCoordsY = []

			nextItem = svgPathsScaled[len(svgPathsScaled)-1]

			while(isFloat(nextItem)):
				x = float(svgPathsScaled.pop()) + float(prevX)
				y = float(svgPathsScaled.pop()) + float(prevY)

				prevX = x
				prevY = y

				bezierCoordsX.append(x)
				bezierCoordsY.append(y)
				nextItem = svgPathsScaled[len(svgPathsScaled)-1]

			for t in range(0, 360-1):
				xBezier = sumBezierElement(len(bezierCoordsX), 0, (1/360)*t, bezierCoordsX)
				yBezier = sumBezierElement(len(bezierCoordsY), 0, (1/360)*t, bezierCoordsY)
				simplePath.append(xBezier)
				simplePath.append(yBezier)
			
		elif pathType == 'Z':
			simplePath.append(startX)
			simplePath.append(startY)
			
		elif pathType == 'l':
			print 'simplePathBefore-l:'
			print simplePath
			prevX = simplePath[len(simplePath)-2]
			prevY = simplePath[len(simplePath)-1]

			nextItem = svgPathsScaled[len(svgPathsScaled)-1]

			while(isFloat(nextItem)):
				x = float(svgPathsScaled.pop()) + float(prevX)
				y = float(svgPathsScaled.pop()) + float(prevY)

				differenceX = getDifference(x,prevX)
				differenceY = getDifference(y,prevY)
				length = m.sqrt(m.pow(differenceX,2) + m.pow(differenceY,2))
				fernandos = int(length/0.0003)
				stepX = differenceX/fernandos
				stepY = differenceY/fernandos
				for fernando in range(0,fernandos):
					simplePath.append(x+float(fernando*stepX))
					simplePath.append(y+float(fernando*stepY))

				prevX = x
				prevY = y
				simplePath.append(x)
				simplePath.append(y)
				nextItem = svgPathsScaled[len(svgPathsScaled)-1]

def getDifference(x, y):
	if x > y:
		return m.fabs(x-y)
	else:
		return m.fabs(y-x)

def binomialCoefficient(n, i):
	#In case you are calculating first Bezier Element
	if i == 0:
		return 1
	return float(m.fak(n)/(m.fak(i)*m.fak(n-i)))

def sumBezierElement(n, i, t, pointList):
	B = binomialCoefficient(n,i) * m.pow(1-t,n-i) * m.pow(t,i) * float(pointList[i-1][0])

	return B + sumBezierElement(n, i+1, t, pointList)

if __name__ == '__main__':
	listOfPaths = svg_parser2.getListOfPaths()
	for x in listOfPaths:
		relativize(x)

	print "The Final Path is: " + str(finalPath)	




