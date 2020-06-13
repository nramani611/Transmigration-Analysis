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
        for tup2 in initialized_list:
            if distance(tup1, tup2) < 20:
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

def UpdatePng(cell_list, png_file):
    for cell in cell_list:
        if cell.get_old_loc() == None:
            break
        else:
            cv2.line(png_file, cell.get_old_loc(), cell.get_current_loc(), (255, 0, 0, 255), 2)
    return png_file

def HistList(list):
    new_list = []
    for i in list:
        for j in i:
             new_list.append(j)
    new_list.sort(reverse = True)
    return new_list

def Display(array, thresh, val):
    x, y = array.shape
    for i in range(x):
        for j in range(y):
            if array[i, j] <= thresh:
                array[i, j] = val

    const = 2
    for i in range(0, const):
        for j in range(y):
            array[i, j] = val
    for i in range(x):
        for j in range(0, const):
            array[i, j] = val
    for i in range(x - const, x):
        for j in range(y):
            array[i, j] = val
    for i in range(x):
        for j in range(y - const, y):
            array[i, j] = val

    for _ in range(2):
        for i in range(2, x - 2):
            for j in range(2, y - 2):
                counter = 0
                if array[i, j] != val:
                    if array[i - 1, j] == val:
                        counter += 1
                    if array[i, j - 1] == val:
                        counter += 1
                    if array[i + 1, j] == val:
                        counter += 1
                    if array[i, j + 1] == val:
                        counter += 1
                    if array[i + 1, j + 1] == val:
                        counter += 1
                    if array[i - 1, j - 1] == val:
                        counter += 1
                    if array[i - 1, j + 1] == val:
                        counter += 1
                    if array[i + 1, j - 1] == val:
                        counter += 1
                    if array[i - 2, j] == val:
                        counter += 1
                    if array[i, j - 2] == val:
                        counter += 1
                    if array[i + 2, j] == val:
                        counter += 1
                    if array[i, j + 2] == val:
                        counter += 1
                    if array[i + 2, j + 2] == val:
                        counter += 1
                    if array[i - 2, j - 2] == val:
                        counter += 1
                    if array[i - 2, j + 2] == val:
                        counter += 1
                    if array[i + 2, j - 2] == val:
                        counter += 1
                    if array[i + 2, j - 1] == val:
                        counter += 1
                    if array[i + 2, j + 1] == val:
                        counter += 1
                    if array[i + 1, j - 2] == val:
                        counter += 1
                    if array[i + 1, j + 2] == val:
                        counter += 1
                    if array[i - 2, j + 1] == val:
                        counter += 1
                    if array[i - 2, j + 1] == val:
                        counter += 1
                    if array[i - 1, j - 2] == val:
                        counter += 1
                    if array[i - 1, j + 2] == val:
                        counter += 1
                    if counter > 22:
                        array[i, j] = val
                #print(counter)

    return array

#Matched Template function for analyzing images
def MatchedTemplate(img, template, method, w, h, png_file, val, cell_list = []):
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
        cv2.putText(img_copy, str(cell.get_cell_number()), (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (209, 80, 0, 255), 2)
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (255, 165, 0), 2)


    png_file = UpdatePng(cell_list, png_file)
    #print(img_copy)


    if val == 28:
        f, ax1 = plt.subplots(1, 1)
        ax1.imshow(img_copy, cmap = 'gray')
        plt.show()
    #hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    #hist = HistList(hist.tolist())
    #hist = hist[::-1]

    #new_hist = []
    #for i in hist:
        #if i < 50:
        #    new_hist.append(i)

    #print(new_hist)
    #x = np.linspace(0, 255, len(new_hist))
    #x = np.flip(x, 0)
    #x = x[:100]
    #print(hist)
    #print(x)
    #ax2.plot(new_hist, x)
    #ax2.set_ylim(0, 50)
    #yints = range(0, 50)
    #ax2.set_major_locator(yints)

    return cell_list
