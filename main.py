from libtiff import TIFFfile
from libtiff import TIFF
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from cell_class import *
from helper_functions import *
import os

meth = 'cv2.TM_CCOEFF'
h_bins = 256

img = cv2.imreadmulti("Composite_1-1.tif")
template = cv2.imread('cell.jpg', 0)
img_list = img[1]
w, h = template.shape[::-1]
w, h = w + 3, h + 3

x, y = img_list[0].shape[::-1]
#print(x, y)
#print(img_list[0].shape[::-1])
png_file = np.zeros((x, y))

cell_list = []
counter = 0

for data in img_list:
    counter += 1
    img = data.copy()
    #print(type(img.shape))

    cell_list = MatchedTemplate(img, template, meth, w, h, png_file, cell_list)

    #Break statement just to test after a set number of iterations
    if counter == 25:
        break
