import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
while(1):
	# Take each frame
	_, frame = cap.read()
	# Convert BGR to HSV
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	# define range of blue color in HSV
	lower_blue = np.array([110,50,50])
	upper_blue = np.array([130,255,255])
	
	lower_green = np.array([60,50,10])
	upper_green = np.array([90,255,240])
	
	lower_red = np.array([150,100,50])
	upper_red = np.array([200,255,255])
	
	# Threshold the HSV image to get only blue colors
	mask = cv.inRange(hsv, lower_blue, upper_blue)
	maskGreen = cv.inRange(hsv, lower_green, upper_green)
	maskRed= cv.inRange(hsv, lower_red, upper_red)
	# Bitwise-AND mask and original image
	res = cv.bitwise_and(frame,frame, mask= mask)
	resGreen = cv.bitwise_and(frame,frame, mask= maskGreen)
	resRed = cv.bitwise_and(frame,frame, mask= maskRed)
	
	cv.imshow('frame',frame)
	cv.imshow('resBlue',res)
	cv.imshow('resGreen',resGreen)
	cv.imshow('resRed',resRed)
	k = cv.waitKey(1)
	if k == 27:
		break
	elif k == ord('x'):
		cv.imwrite("fotoBlue.png",res)
		cv.imwrite("fotoGreen.png",resGreen)
		cv.imwrite("fotoRed.png",resRed)
cv.destroyAllWindows()
