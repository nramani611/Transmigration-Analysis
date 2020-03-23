from libtiff import TIFFfile
from libtiff import TIFF
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import cell_class as cell
from helper_functions import *

img = cv2.imreadmulti("Composite_1-1.tif")
template = cv2.imread('cell.jpg', 0)
img_list = img[1]
w, h = template.shape[::-1]
w, h = w + 3, h + 3

meth = 'cv2.TM_CCOEFF'
counter = 0
h_bins = 256

data1 = img_list[0]

match_locations = MatchedTemplate(data1, template, meth, w, h)[0]

cell_list = []
for tup in match_locations:
    cell_list.append(cell.Cell(tup))

img_list = img_list[1:]

for data in img_list:
    counter += 1
    img = data.copy()

    cell_list = MatchedTemplate(img, template, meth, w, h, cell_list)

    #cv2.imwrite("example.png", img)

    #cell_list = TrackCells(cell_list, match_locations)

    #Break statement just to test first iteration
    if counter == 10:
        break
