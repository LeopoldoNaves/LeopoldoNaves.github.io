
# import the opencv module
import cv2 as cv

# capturing video
capture = cv.VideoCapture("./videos/chico-lento.mp4")

backSub = cv.createBackgroundSubtractorMOG2()

#video write
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT) # float
# Define Video Frame Rate in fps
fps = 30

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('chico-lento.avi', fourcc, fps, (int(width),int(height)) )

##########
if not capture.isOpened():
 print('Unable to open: ' + args.input)
 exit(0)

while True:
 ret, frame = capture.read()
 if frame is None:
   break
 
 fgMask = backSub.apply(frame)
 
 
 cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
 cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
 cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
 
 
 cv.imshow('Frame', frame)
 cv.imshow('FG Mask', fgMask)
 fgMask_rgb = cv.cvtColor(fgMask, cv.COLOR_GRAY2RGB)
 out.write(fgMask_rgb)
 
 
 keyboard = cv.waitKey(30)
 if keyboard == 'q' or keyboard == 27:
   break
