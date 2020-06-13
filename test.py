import cv2
import numpy as np
from helper_functions import *
from matplotlib import pyplot as plt

img = cv2.imread("Composite_1-1-Red.tif", 1)


b, g, r = cv2.split(img)

cv2.imshow('example', r)
cv2.waitKey(0)
cv2.destroyAllWindows()


r = Display(r, 100, 255)

hist = cv2.calcHist([r], [0], None, [256], [0, 256])
hist = HistList(hist.tolist())
hist = hist[::-1]
#print(hist)

#for i in img:
#    for j in i:
#        if j != 0:
#            print(j)

new_hist = []
for i in hist:
    if i < 150 and i > 100:
        new_hist.append(i)

#print(new_hist)
x = np.linspace(0, 255, len(new_hist))
x = np.flip(x, 0)
#x = x[:100]

plt.plot(new_hist, x)
#plt.show()

cv2.imshow('example', r)
cv2.waitKey(0)
cv2.destroyAllWindows()
