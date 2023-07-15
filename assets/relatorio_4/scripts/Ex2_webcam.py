import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)
while (1):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', frame)
    cv.imshow('gray', gray)

    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('x'):
        cv.imwrite('fotoFrame.png', frame)
        img = cv.imread('fotoFrame.png', cv.IMREAD_GRAYSCALE)
        assert img is not None, "file could not be read, check with os.path.exists()"
        hist, bins = np.histogram(img.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * float(hist.max()) / cdf.max()
        equ = cv.equalizeHist(img)
        res = np.hstack((img, equ))  # stacking images side-by-side
        cv.imshow('res', res)

cap.release()

k = cv.waitKey(0)
if k == ord("x"):
    cv.imwrite('result.png', res)

plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.savefig('histogram.png')
plt.show()

plt.plot(cdf_normalized, color = 'g')
plt.hist(equ.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.savefig('histogram_equalized.png')
plt.show()



cv.destroyAllWindows()
