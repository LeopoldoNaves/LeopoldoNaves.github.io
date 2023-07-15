import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('normal_and_equalizer.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
hist,bins = np.histogram(img.flatten(),256,[0,256])
cdf = hist.cumsum()
cdf_normalized = cdf * float(hist.max()) / cdf.max()
equ = cv.equalizeHist(img)
res = np.hstack((img,equ)) #stacking images side-by-side
cv.imshow('res',res)
k = cv.waitKey(0)
if k == ord('x'):
    cv.imwrite('normal.jpeg', res)

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

