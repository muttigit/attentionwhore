#!/usr/bin/env python
import re

def parseSVGFile(svgFilePath):
	svgFile = open(svgFilePath)
	svgFileLines = svgFile.readlines()
	svgFile.close()

	for svgLine in svgFileLines:
		pathLines = re.search('d=', svgLine)
		
		print svgLine
		
		if pathLines == None:
			print "NOPE"
		
		#print 'pathLines-Size: ' + len(pathLines)
		#for pathLine in pathLines:
			#print pathLine
	#print 'svgLines-Size: ' + len(svgLines)

if __name__ == '__main__':
	print 'Hello world'
	parseSVGFile('/home/josch/ros_sandbox/attentionwhore/attentionwhore_logo.svg')
