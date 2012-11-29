#!/usr/bin/env python

def relativize(svgPaths):
	""" Relativize maximum to 20cm? """
	
	
	""" Read and push coordinates """
	svgPaths.reverse()
	while(len(svgPaths) != 0):
		pathType = svgPaths.pop()
		if pathType == 'M':
			x = svgPaths.pop()
			y = svgPaths.pop()
			tripel = ['m', x, y]
			print tripel
		elif pathType == 'm':
			print 'm'
		elif pathType == 'C':
			print 'C'
		elif pathType == 'c':
			print 'c'
		elif pathType == 'Z':
			print 'Z'
		elif pathType == 'z':
			print 'z'
		elif pathType == 'l':
			print 'l'
		elif pathType == 'zm':
			print 'zm'
if __name__ == '__main__':
	"""main"""
	list_path = ['M', 4, 3, 'c', 10, 11, 'M', 5, 6]
	relativize(list_path)
