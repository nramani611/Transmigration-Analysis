from libtiff import TIFFfile
from libtiff import TIFF
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import cell_class as cell


img = cv2.imreadmulti("Composite_1-1.tif")
template = cv2.imread('cell.jpg', 0)
img_list = img[1]
w, h = template.shape[::-1]
w, h = w + 3, h + 3

meth = 'cv2.TM_CCOEFF'
counter = 0
h_bins = 256

#Helper Functions
def list_2_tuple(list1, list2):
    tup_list = []
    for i in range(len(list1)):
        tup = (list1[i], list2[i])
        tup_list.append(tup)
    return tup_list

def distance(tup1, tup2):
    return math.sqrt((tup2[1] - tup1[1])**2 + (tup2[0] - tup1[0])**2)

def UniqueHits(zip_list, initialized_list):

    for tup1 in zip_list:
        counter = 0
        for tup2 in initialized_list:
            if distance(tup1, tup2) < 20:
                #counter += 1
                break
        else:
            initialized_list.append(tup1)
    return initialized_list

def TrackCells(cell_list, match_locations):
    for cell in cell_list:
        new_cell_list = []
        min_dist = np.inf
        current_index = -1

        for i in range(len(match_locations)):
            dist = distance(cell.get_current_loc(), match_locations[i])
            if dist < min_dist:
                min_dist = dist
                current_index = i

        print(len(match_locations), current_index)

        try:
            cell.set_loc(match_locations.pop(current_index))
            new_cell_list.append(cell)

        except IndexError:
            break


    return cell_list

#Matched Template function for analyzing images
def MatchedTemplate(img, template, method):
    img_copy = img.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    min_thresh = (min_val + 1e-6) * .60
    match_locations = np.where(res <= min_thresh)

    match_locations = list_2_tuple(list(match_locations[0]), list(match_locations[1]))
    initialized_list = [match_locations[0]]

    match_locations  = UniqueHits(match_locations, initialized_list)

    for tup in match_locations:
        x, y = tup[1], tup[0]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 165, 0), 2)

    f, ax1 = plt.subplots(1, 1)
    ax1.imshow(img, cmap = 'gray')
    plt.show()

    return match_locations

data1 = img_list[0]

match_locations = MatchedTemplate(data1, template, meth)

cell_list = []
for tup in match_locations:
    cell_list.append(cell.Cell(tup))

img_list = img_list[1:]

for data in img_list:
    img = data.copy()

    match_locations = MatchedTemplate(img, template, meth)

    cv2.imwrite("example.png", img)

    cell_list = TrackCells(cell_list, match_locations)

    for cell in cell_list:
        print(cell)

    #Break statement just to test first iteration
    break
