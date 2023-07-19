
# import the opencv module
import cv2 as cv

# capturing video
capture = cv.VideoCapture(0)

backSub = cv.createBackgroundSubtractorMOG2()

#backSub = cv.createBackgroundSubtractorKNN()
#video write
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT) # float
# Define Video Frame Rate in fps
fps = 15

fourcc = cv.VideoWriter_fourcc(*'XVID')
out1 = cv.VideoWriter('limpo.avi', fourcc, fps, (int(width),int(height)) )
out2 = cv.VideoWriter('mascara.avi', fourcc, fps, (int(width),int(height)) )

##########
if not capture.isOpened():
 print('Unable to open: ' + args.input)
 exit(0)

while True:
 ret, frame = capture.read()
 #frame = cv.flip(frame,0)
 #frame = cv.flip(frame,1)
 if frame is None:
   break
 
 fgMask = backSub.apply(frame)
 
 
 cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
 cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
 cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
 
 
 cv.imshow('Frame', frame)
 cv.imshow('FG Mask', fgMask)
 fgMask_rgb = cv.cvtColor(fgMask, cv.COLOR_GRAY2RGB)
 out1.write(frame)
 out2.write(fgMask_rgb)
 
 
 keyboard = cv.waitKey(30)
 if keyboard == 'q' or keyboard == 27:
   break
