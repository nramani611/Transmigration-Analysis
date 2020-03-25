from libtiff import TIFFfile
from libtiff import TIFF
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from cell_class import *

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

    while len(match_locations) != 0:
        target_loc = match_locations.pop()
        current_dist = np.inf

        for index in range(len(cell_list)):
            dist = distance(cell_list[index].get_current_loc(), target_loc)
            if dist < current_dist:
                ind = index
                current_dist = dist

        if current_dist > 20:
            continue

        try:
            target_cell = cell_list.pop(ind)
            target_cell.set_loc(target_loc)
            new_cell_list.append(target_cell)

        except ValueError:
            continue

        except IndexError:
            continue


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

    if cell_list == []:
        for tup in match_locations:
            cell_list.append(Cell(tup))
    else:
        cell_list = TrackCells(cell_list, match_locations)

    for cell in cell_list:
        x, y = cell.get_current_loc()[1], cell.get_current_loc()[0]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 165, 0), 2)

    print(len(cell_list))

    f, ax1 = plt.subplots(1, 1)
    ax1.imshow(img, cmap = 'gray')
    plt.show()

    return cell_list
