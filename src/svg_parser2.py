#!/usr/bin/env python

#if __name__=="__main__":
def getListOfPaths ():
	svgcode = ""
	paths = []
	svgfile = open("attentionwhore_logo.svg", "r")
	for line in svgfile:
		svgcode += line
	endPos = 0
	
	"""startPosW = svgcode.find('''width="''') + 7
	if startPosW != -1:
		endPosW = svgcode.find('''"''', startPosW)
		path.append(svgcode[startPosW:endPosW-1])
		print svgcode[startPosW:endPosW-1]
		
		startPosH = svgcode.find('''height="''') + 8
		endPosH = svgcode.find('''"''', startPosW)
		path.append(svgcode[startPosH:endPosH-1])
		print svgcode[startPosH:endPosH-1]"""

	while( True):	
		startPos = svgcode.find("<path id=", endPos)
		if startPos == -1:
			break
		startPos = svgcode.find(" d=", startPos)
		endPos = svgcode.find("\"/>", startPos)
		path = svgcode[startPos+4:endPos]
		#path = path.replace("zm", "#y") PATH zm IS NOT A PATH
		path = path.replace("M", "#M#")
		path = path.replace("m", "#m#")
		path = path.replace("Z", "#Z#")
		path = path.replace("z", "#Z#")
		path = path.replace("C", "#C#")
		path = path.replace("c", "#c#")
		path = path.replace("l", "#l#")
		path = path.replace(" ", ",")
		path = path.replace(",","#")
		path = path.split("#")
#		for i in range(len(path)):
#			path[i] = path[i].split(",")
#			path[i].insert(0, path[i][0][0:1])
#			path[i][1] = path[i][1][1:len(path[i][1])]
#			'''if path[i][0] == "y":
#				path[i][0] = "zm"'''
#		del path[0]
		paths.append(path)

	return paths 
#	for i in range(len(paths)):
#		for j in range(len(paths[i])):
#			print paths[i][j]
#	pass

