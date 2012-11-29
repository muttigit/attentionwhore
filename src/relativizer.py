#!/usr/bin/env python

minVal = 0
maxVal = 0

finalPath = []

def minMaxAbs(val):
	global minVal
	global maxVal
	
	if val > maxVal:
		maxVal = val
	if val < minVal:
		minVal = val

def minMaxRel(val):
	print 'Hello'

def relativize(svgPaths):
	startX
	startY
	
	global finalPath = []
	
	"""	Read and push coordinates
		Check for min and max Values
	"""
	
	svgPaths.reverse()
	while(len(svgPaths) != 0):
		pathType = svgPaths.pop()
		if pathType == 'M':
			x = svgPaths.pop()
			y = svgPaths.pop()
			startX = x
			startY = y
			tripel = ['M', x, y]
			
			finalPath.append(tripel)
			
			minMaxAbs(x)
			minMaxAbs(y)
			
			print simplePath
		elif pathType == 'm':
			prevX = finalPath[len(finalPath)] - 2
			prevY = finalPath[len(finalPath)] - 1
			
			x = svgPaths.pop() + prevX
			y = svgPaths.pop() + prevY
			simplePath = ['M', x, y]
			
			finalPath.append(simplePath)
			
			minMaxAbs(x)
			minMaxAbs(y)
			
			print simplePath
		elif pathType == 'C':
			#Bézier Curve Poles
			x1 = svgPaths.pop()
			y1 = svgPaths.pop()
			x2 = svgPaths.pop()
			y2 = svgPaths.pop()
			#Target Point
			x = svgPaths.pop()
			y = svgPaths.pop()
			
			simplePath = ['D', x1, y1, x2, y2, x, y]
			
			finalPath.append(simplePath)
			
			minMaxAbs(x1)
			minMaxAbs(y1)
			minMaxAbs(x2)
			minMaxAbs(y2)
			minMaxAbs(x)
			minMaxAbs(y) 
			
			print simplePath
		elif pathType == 'c':
			prevX = finalPath[len(finalPath)] - 2
			prevY = finalPath[len(finalPath)] - 1
			
			#Bézier Curve Poles
			x1 = svgPaths.pop() + prevX
			y1 = svgPaths.pop() + prevY
			x2 = svgPaths.pop() + prevX
			y2 = svgPaths.pop() + prevY
			#Target Point
			x = svgPaths.pop() + prevX
			y = svgPaths.pop() + prevY
			
			simplePath = ['D', x1, y1, x2, y2, x, y]
			
			finalPath.append(simplePath)
			
			minMaxAbs(x1)
			minMaxAbs(y1)
			minMaxAbs(x2)
			minMaxAbs(y2)
			minMaxAbs(x)
			minMaxAbs(y) 
			
			print simplePath
		elif pathType == 'Z':
			simplePath = ['D', startX, startY]
			
			finalPath.append(simplePath)
			
			print simplePath
		elif pathType == 'z':
			simplePath = ['D', startX, startY]
			
			finalPath.append(simplePath)
			
			print simplePath
		elif pathType == 'l':
			prevX = finalPath[len(finalPath)] - 2
			prevY = finalPath[len(finalPath)] - 1
			
			x = svgPaths.pop() + prevX
			y = svgPaths.pop() + prevY
			
			simplePath = ['D', x, y]
			
			finalPath.append(simplePath)
			
			minMaxAbs(x)
			minMaxAbs(y) 
			
			print simplePath		
	
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
	list_path = ['M', 4, 3, 'c', 10, 11, 'M', 5, 6]
	relativize(list_path)
