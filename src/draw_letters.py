#!/usr/bin/env python

import roslib; roslib.load_manifest('attentionwhore')
import rospy
from toolset2draw import draw_letter, visual_control, build_paths, fill_scaling_gaps, safeImage, relativizer, print_paths, talker
from PIL import ImageFont

if __name__ == "__main__":
	letter = "M"
	lettersize = 70 #170 #70 nice for letters, 70, 5, 4000
	scalingFactor = 3#3#5#3
	resizeFactor = 1#0.5#1#5
	relativizFactor = 4000 #4000
	safePath = "Test.png"
	font = ImageFont.truetype("fonts/Helv25.ttf", lettersize)
	#font = ImageFont.truetype("Arial.ttf", lettersize)
	
	size_and_pix = draw_letter(letter, font, resizeFactor)
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
