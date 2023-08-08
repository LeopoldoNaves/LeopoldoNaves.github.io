import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

width = cap.get(cv.CAP_PROP_FRAME_WIDTH) * 2   # float
# Get current height of frame
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT) # float
# Define Video Frame Rate in fps
fps =  15

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('lab6d_A.avi', fourcc, fps, (int(width),int(height)) )

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frameRaw = frame.copy()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv.cornerHarris(gray,2,3,0.04)
    dst = cv.dilate(dst,None)

    frame[dst>0.01*dst.max()]=[0,0,255]
    
    # Display the resulting frame
    merge = np.concatenate((frameRaw, frame), axis = 1)
    cv.imshow('frame', merge)
    out.write(merge)    
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
