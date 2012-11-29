#!/usr/bin/env python

import roslib; roslib.load_manifest('attentionwhore')
import rospy
from attentionwhore.msg import Trajectory
from attentionwhore.msg import Point
#from std_msgs.msg import String
from PIL import Image, ImageDraw, ImageFont

def draw_letter(letter, font, resizeFactor):
	image = Image.new("1", (1,1), 0)
	size = ImageDraw.Draw(image).textsize(letter, font=font)
	image = image.resize(size)
	ImageDraw.Draw(image).text((0,0), letter, font=font, fill=1)
	if resizeFactor > 1:
		size = (size[0]*resizeFactor, size[1]*resizeFactor)
		image = image.resize((size[0], size[1]))
	pix = image.load()
	return size, pix

def invert_pic(size, pix):
	for i in range(size[0]):
		for j in range(size[1]):
			if pix[i,j] == 0:
				pix[i,j] = 1
			else:
				pix[i,j] = 0
	return pix
	
def draw_picture(picturePath, invert, resizeFactor):
	image = Image.open(picturePath)
	size = image.size
	if resizeFactor > 1:
		size = (size[0]*resizeFactor, size[1]*resizeFactor)
		image = image.resize((size[0], size[1]))
	pix = image.load()
	if invert:
		pix = invert_pic(size, pix)
	return size, pix

def visual_control(pix, size):
	pic = []
	for y in range(size[1]):
		line = []
		for x in range(size[0]):
			line.append(pix[x, y])
		if not sum(line) == 0:
			pic.append(line)
		#pic.append(line)

	for i in range(len(pic)):
		for j in range(len(pic[i])):
			if pic[i][j]:
				print "#",
			else:
				print "''''",
		print ""
	if not len(pic) == 0:
		print len(pic)
		print len(pic[0])
	pass

def build_paths(pix, scalingFactor):
	searchPos = ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))
	paths = []
	
	while True:
		foundStartPoint = False
		xNow = 0
		yNow = 0
		path = []
		for y in range(size[1]):
			for x in range(size[0]):
				if (pix[x, y]):
					foundStartPoint = True
					xNow = x
					yNow = y
					#
					path.append((xNow*scalingFactor, yNow*scalingFactor))
					pix[xNow, yNow] = 0
					break
			if (foundStartPoint):
				break
		while True:
			xOld = xNow
			yOld = yNow
			for i in range(len(searchPos)):
				try:
					if (pix[xNow + searchPos[i][0], yNow + searchPos[i][1]]):
						xNow = xNow + searchPos[i][0]
						yNow = yNow + searchPos[i][1]
						path.append((xNow*scalingFactor, yNow*scalingFactor))
						pix[xNow, yNow] = 0
						break
				except:
					pass
			if (xNow, yNow)	== (xOld, yOld):
				break
		#print path
		paths.append(path)
		if not foundStartPoint:
			break

	for i in range(len(paths)-3, -1, -1):
		#print (paths[i][0][0]-paths[i+1][len(paths[i+1])-1][0])
		if abs(paths[i][0][0]-paths[i+1][0][0])==scalingFactor and abs(paths[i][0][1]-paths[i+1][0][1])==scalingFactor:
			paths[i+1].reverse()
			paths[i] = paths[i+1] + paths[i]
			del paths[i+1]
		elif abs(paths[i][0][0]-paths[i+1][len(paths[i+1])-1][0])<scalingFactor+1 and abs(paths[i][0][1]-paths[i+1][len(paths[i+1])-1][1])<scalingFactor+1:
			paths[i] = paths[i+1] + paths[i]
			del paths[i+1]
	return paths

def fill_scaling_gaps(paths, scalingFactor):
	newPaths = []
	for i in range(len(paths)):
		path = []
		for j in range(len(paths[i])):
			x0 = paths[i][j][0]
			y0 = paths[i][j][1]
			path.append((x0,y0))
			try:
				y1 = paths[i][j+1][1]
				x1 = paths[i][j+1][0]
				if x0 == x1:
					if y0 < y1:
						for k in range(1, scalingFactor):
							path.append((x0,y0+k))
					else:
						for k in range(1, scalingFactor):
							path.append((x0,y0-k))
				elif y0 == y1:
					if x0 < x1:
						for k in range(1, scalingFactor):
							path.append((x0+k,y0))
					else:
						for k in range(1, scalingFactor):
							path.append((x0-k,y0))
				elif x0 + y0 == x1 + y1:
					if x0 < x1:
						for k in range(1, scalingFactor):
							path.append((x0+k,y0-k))
					else:
						for k in range(1, scalingFactor):
							path.append((x0-k,y0+k))
				else:
					if x0 < x1:
						for k in range(1, scalingFactor):
							path.append((x0+k,y0+k))
					else:
						for k in range(1, scalingFactor):
							path.append((x0-k,y0-k))
			except:
				pass
		newPaths.append(path)
	return newPaths
	pass
	
def safeImage(paths, size, scalingFactor, safePath):
	image = Image.new("RGB", (size[0]*scalingFactor, size[1]*scalingFactor))
	for i in range(len(paths)):
		for j in range(len(paths[i])):
			image.putpixel((paths[i][j][0], paths[i][j][1]), (255,0,0))
	image.save(safePath)

def relativizer(paths, relativizFactor):
	newPaths = []
	for i in range(len(paths)):
		newPath = []
		for j in range(len(paths[i])):
			x = paths[i][j][0] / float(relativizFactor)
			y = paths[i][j][1] / float(relativizFactor)
			if x > 0.22:
				print "Error x"
				print x
			if y > 0.182:
				print "Error y"
				print y
			newPath.append((x, y))
		newPaths.append(newPath)
	#print newPaths
	return newPaths
	

def print_paths(paths):
	for i in range(len(paths)):
		print paths[i]
	print len(paths)

	
def talker(paths):
	#pub = rospy.Publisher('/string', String)
	pub = rospy.Publisher('/trajectory', Trajectory)
	rospy.init_node('ik_solver_talker')
	rospy.sleep(0.5)
	for i in range(len(paths)-1):
		if rospy.is_shutdown():
			break
		traject = Trajectory()
		for j in range(len(paths[i])):
			p = Point(paths[i][j][0],paths[i][j][1])
			traject.trajectory.append(p)
			#print traject.trajectory
		pub.publish(traject)
		rospy.sleep(5)
		rospy.loginfo(traject)


if __name__ == "__main__":
	letter = "Buhu"
	lettersize = 70 #170 #70
	scalingFactor = 5#3
	resizeFactor = 1#5
	relativizFactor = 4000
	font = ImageFont.truetype("fonts/Helv25.ttf", lettersize)
	#font = ImageFont.truetype("Arial.ttf", lettersize)
	picturePath = "pictures/pirate.bmp"
	safePath = "Test.png"
	invert = True
	
	size_and_pix = draw_letter(letter, font, resizeFactor)
	#size_and_pix = draw_picture(picturePath, invert, resizeFactor)
	
	size = size_and_pix[0]
	pix = size_and_pix[1]
	#visual_control(pix, size)
	paths = build_paths(pix, scalingFactor)
	if scalingFactor > 1:
		paths = fill_scaling_gaps(paths, scalingFactor)
	safeImage(paths, size, scalingFactor, safePath)
	paths = relativizer(paths, relativizFactor)
	#print_paths(paths)
	talker(paths)
