import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('leo_chico.png')
assert img is not None, "file could not be read, check with os.path.exists()"


imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

redChannel= imgRGB[:,:,0:1]
greenChannel = imgRGB[:,:,1:2]
blueChannel = imgRGB[:,:,2:3]


histRed,bins = np.histogram(redChannel.flatten(),256,[0,256])
cdfRed = histRed.cumsum()
cdf_normalizedRed = cdfRed * float(histRed.max()) / cdfRed.max()
equRed= cv.equalizeHist(redChannel)

histGreen,bins = np.histogram(greenChannel.flatten(),256,[0,256])
cdfGreen = histGreen.cumsum()
cdf_normalizedGreen = cdfGreen * float(histGreen.max()) / cdfGreen.max()
equGreen = cv.equalizeHist(greenChannel)


histBlue,bins = np.histogram(blueChannel.flatten(),256,[0,256])
cdfBlue = histBlue.cumsum()
cdf_normalizedBlue = cdfBlue * float(histBlue.max()) / cdfBlue.max()
equBlue = cv.equalizeHist(blueChannel)


equRGB = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
equRGB[:,:,0] = equRed
equRGB[:,:,1] = equGreen
equRGB[:,:,2] = equBlue







res = np.hstack((imgRGB,equRGB)) #stacking images side-by-side
res = cv.cvtColor(res, cv.COLOR_RGB2BGR)
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

