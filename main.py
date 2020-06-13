import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from cell_class import *
from helper_functions import *
import glob

meth = 'cv2.TM_CCOEFF'
h_bins = 256

img = cv2.imreadmulti("Composite_1-1.tif")
img_list = img[1]
x, y = img_list[0].shape[::-1]
png_file = np.zeros((x, y))
cell_list = []

f, ax1 = plt.subplots(1, 1)
ax1.imshow(img_list[0], cmap = 'gray')
plt.show()

path = glob.glob("Cell_Templates/*.png")

counter = 0

#image = img_list[0]
#lower_red = np.array([178, 179, 0])
#upper_red = np.array([255, 255, 255])
#hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#mask = cv2.inRange(image, lower_red, upper_red)
#coord = cv2.findNonZero(mask)
#print(coord)

for data in img_list:
    counter += 1
    img = data.copy()

    for file in path:
        template = cv2.imread(file, 0)
        #print(template)
        w, h = template.shape[::-1]
        w, h = w + 3, h + 3

        cell_list = cell_list + MatchedTemplate(img, template, meth, w, h, png_file, counter, cell_list)

    temp_cell_list = cell_list[1:]
    cell_list = [cell_list[0]]

    for cell1 in temp_cell_list:
        for cell2 in cell_list:
            if distance(cell1.get_current_loc(), cell2.get_current_loc()) < 5:
                break
        else:
            cell_list.append(cell1)

    print(counter, len(cell_list))

    if len(cell_list) != 15:
        print("Did not reach end")
        break

    #Break statement just to test after a set number of iterations
    #if counter == 15:
    #    break
