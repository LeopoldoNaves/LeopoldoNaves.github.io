import cv2

cap = cv2.VideoCapture("./videos/Leopoldo_rapido.mp4")

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
# Define Video Frame Rate in fps
fps = 30

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./output/ex1c/Leopoldo_rapido.avi', fourcc, fps, (int(width),int(height)) )


mog = cv2.createBackgroundSubtractorKNN()

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
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
    
    img_1 = cv2.flip(frame,0)
    img_1 = cv2.flip(img_1,1)
    out.write(img_1)
    
    
    cv2.imshow('Motion Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
