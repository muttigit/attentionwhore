#!/usr/bin/env python
import re

def parseSVGFile(svgFilePath):
	svgFile = open(svgFilePath)
	svgFileLines = svgFile.readlines()
	svgFile.close()

	for svgLine in svgFileLines:
		pathRegExp = re.compile('''(d=")([a-zA-Z]{1,2}([\+\-]?\d+(\.\d+)?[\s,]?)*)*("/>)''')
		pathRegExp2 =  re.compile('''(d=")([a-zA-Z]{1,2}(((\+|\-)?(\d+|\.\d+)|\s|,)*))*"/>''')
		pathLines = pathRegExp.findall(svgLine)	
		
		print pathLines
		
		if pathLines == None:
			print "NOPE"
		#else:
			#for pathLine in pathLines:
				#print pathLine
	#print 'svgLines-Size: ' + len(svgLines)

if __name__ == '__main__':
	print 'Hello world'
	parseSVGFile('/home/josch/ros_sandbox/attentionwhore/attentionwhore_logo.svg')
