from libtiff import TIFFfile
from libtiff import TIFF
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import cell_class as cell

def list_2_tuple(list1, list2):
    tup_list = []
    for i in range(len(list1)):
        tup = (list1[i], list2[i])
        tup_list.append(tup)
    return tup_list

def distance(tup1, tup2):
    return math.sqrt((tup2[1] - tup1[1])**2 + (tup2[0] - tup1[0])**2)

def UniqueHits(zip_list):
    initialized_list = [zip_list[0]]

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
    new_cell_list = []

    for i in range(len(match_locations)):
        all_dist = []
        #min_dist = np.inf
        #current_index = -1

        for cell in cell_list:
            dist = distance(cell.get_current_loc(), match_locations[i])
            all_dist.append(dist)
            #if dist < min_dist:
            #    min_dist = dist
            #    current_index = i

        try:
            target_cell = cell_list.pop(all_dist.index(min(all_dist)))
            target_cell.set_loc(match_locations[i])
            print(target_cell)
            #cell.set_loc(match_locations.pop(current_index))
            new_cell_list.append(target_cell)

        except IndexError:
            break

        #print(len(new_cell_list))


    return new_cell_list

#Matched Template function for analyzing images
def MatchedTemplate(img, template, method, w, h, cell_list = []):
    img_copy = img.copy()
    method = eval(method)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    min_thresh = (min_val + 1e-6) * .60
    match_locations = np.where(res <= min_thresh)

    match_locations = list_2_tuple(list(match_locations[0]), list(match_locations[1]))
    match_locations  = UniqueHits(match_locations)

    if cell_list != []:
        cell_list = TrackCells(cell_list, match_locations)

    for cell in cell_list:
        x, y = cell.get_current_loc()[1], cell.get_current_loc()[0]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 165, 0), 2)

    f, ax1 = plt.subplots(1, 1)
    ax1.imshow(img, cmap = 'gray')
    plt.show()

    return (match_locations, cell_list)
