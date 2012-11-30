#!/usr/bin/env python

import roslib; roslib.load_manifest('attentionwhore')
import rospy
from toolset2draw import draw_picture, visual_control, build_paths, fill_scaling_gaps, safeImage, relativizer, print_paths, talker

if __name__ == "__main__":
	scalingFactor = 1#3#5#3
	resizeFactor = 1#0.2#1#5
	relativizFactor = 4100 #4100
	safePath = "Test1.png"
	invert = True
	picturePath = "pictures/Greetings.bmp"
	#picturePath = "pictures/phoenix_bw.bmp"
	
	size_and_pix = draw_picture(picturePath, invert, resizeFactor)	
	size = size_and_pix[0]
	pix = size_and_pix[1]
	#visual_control(pix, size)
	paths = build_paths(pix, scalingFactor, size)
	if scalingFactor > 1:
		paths = fill_scaling_gaps(paths, scalingFactor)
	safeImage(paths, size, scalingFactor, safePath)
	paths = relativizer(paths, relativizFactor)
	#print_paths(paths)
	talker(paths)
