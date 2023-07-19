import cv2

cap = cv2.VideoCapture(0)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
# Define Video Frame Rate in fps
fps = 15
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('retangle.avi', fourcc, fps, (int(width),int(height)) )
out2 = cv2.VideoWriter('limpo.avi', fourcc, fps, (int(width),int(height)) )
out3 = cv2.VideoWriter('mascara.avi', fourcc, fps, (int(width),int(height)) )








#mog = cv2.createBackgroundSubtractorMOG2()
mog = cv2.createBackgroundSubtractorKNN()

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_clear = frame
    
    fgmask = mog.apply(gray)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Ignore small contours
        if cv2.contourArea(contour) < 1000:
            continue
        
        # Draw bounding box around contour
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    
    #out.write(frame)
    
    frame = cv2.flip(frame,1)
    cv2.imshow('Motion Detection', frame)
    out.write(frame)
    out2.write(fgmask)
    out3.write(frame_clear)
    if cv2.waitKey(1) == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
