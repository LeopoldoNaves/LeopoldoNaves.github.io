# import the opencv module
import cv2 as cv

# capturing video
capture = cv.VideoCapture(0)


#backSub = cv.createBackgroundSubtractorKNN()
#video write
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT) # float
# Define Video Frame Rate in fps
fps = 30

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('./output/ex1b/Leopoldo_rapido.avi', fourcc, fps, (int(width),int(height)) )





while capture.isOpened():
    # to read frame by frame
    _, img_1 = capture.read()
    _, img_2 = capture.read()

    # find difference between two frames
    diff = cv.absdiff(img_1, img_2)

    # to convert the frame to grayscale
    diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)

    # apply some blur to smoothen the frame
    diff_blur = cv.GaussianBlur(diff_gray, (5, 5), 0)

    # to get the binary image
    _, thresh_bin = cv.threshold(diff_blur, 20, 255, cv.THRESH_BINARY)

    # to find contours
    contours, hierarchy = cv.findContours(thresh_bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # to draw the bounding box when the motion is detected
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if cv.contourArea(contour) > 300:
            cv.rectangle(img_1, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # cv.drawContours(img_1, contours, -1, (0, 255, 0), 2)
    #img_1 = cv.flip(img_1,0)
    #img_1 = cv.flip(img_1,1)
    #out.write(img_1)
    # display the output
    cv.imshow("Detecting Motion...", img_1)
    if cv.waitKey(100) == 13:
        exit()
