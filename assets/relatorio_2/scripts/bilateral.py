import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
kernel = np.ones((5,5), np.float32)/25

active = False

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Display the resulting frame
    if active:
    	dst = cv.bilateralFilter(frame,9,75,75)
    else:
    	dst = frame
    cv.imshow('dst', dst)
    
    if cv.waitKey(1) == ord('q'):
        break
    elif cv.waitKey(1) == ord('x'):
    	if active:
    		cv.imwrite('dst_blur.png', frame)
    	else:
    		cv.imwrite('dst_limpa.png', frame)
    elif cv.waitKey(1) == ord('t'):
    	active = True
    elif cv.waitKey(1) == ord('f'):
    	active = False
    print(active)
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
