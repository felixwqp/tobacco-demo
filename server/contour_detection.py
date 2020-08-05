
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from skimage import morphology,draw
from skimage.morphology import medial_axis
from collections import defaultdict




def get_stats(point):
    dis = [None] * len(point)
    for i in range(len(point)):
        dis[i] = point[i][2]
    mean_dis = np.mean(dis)
    var_dis = np.var(dis)
    return [mean_dis, var_dis]


def start(image):
    # image group transmitted to the front-end client. 
    images = []

    # convert to RGB
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    # create a binary thresholded image
    _, binary = cv.threshold(gray, 225, 255, cv.THRESH_BINARY_INV)

    images.append({'name':'binary version', 'filename':'binary.png', 'file':binary})

    # find the contours from the thresholded image
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


    # Find the max Contour Area
    max_area = -1
    max_area_idx = 0
    area_record = [0] * len(contours)
    for i in range(len(contours)):
        temp_area = cv.contourArea(contours[i])
        area_record[i] = temp_area
        if max_area < temp_area:
            max_area = temp_area
            max_area_idx = i

    # the contour
    contour_image = cv.drawContours(image, contours, -1, (0, 255, 0))

    images.append({'name':'origin contour', 'filename':'contour_init.png', 'file':contour_image})

    # Contour Selection By Area
    new_contours = []

    print('=====================================')
    print('Average Width of Each Tabacco Strand')

    for i in range(len(contours)):
        if area_record[i] >= max_area * 0.1 and area_record[i] <= max_area * 0.2:
            cnt = contours[i]
            new_contours.append(cnt)
            width_cnt = cv.contourArea(cnt) / cv.arcLength(cnt, True) * 2
            print('Avg Width: Area/arcLength * 2 : ', width_cnt)

    # empty image
    image[...] = 0

    # get filled contour for image.
    image = cv.drawContours(image, new_contours, -1, (0, 255, 0), cv.FILLED)

    images.append({'name':'selected contour', 'filename':'contour_selected.png', 'file':image})
    # convert to RGB
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)


    # Erosion and dilation and Gaussian Blur
    blur = ((5, 5), 1)
    erode_ = (10, 10)
    dilate_ = (20, 20)
    gray = cv.erode(cv.dilate(cv.GaussianBlur(gray, blur[0], blur[1]), np.ones(dilate_)), np.ones(erode_), 1)

    images.append({'name':'refined contour', 'filename':'contour_refined.png', 'file':gray})


    # Selection the skeleton and the corresponding distance.
    skel, distance = medial_axis(gray, return_distance=True)

    # erode and dilate for skeleton
    erode_skel_20 = (20, 20)
    erode_skel_5 = (5, 5)
    erode_skel_10 = (10, 10)
    dilate_skel = (10, 10)

    skel_float = skel.astype(float)

    skel_dilate = cv.dilate(skel_float, np.ones(dilate_skel))
    skel_erode_20 = cv.erode(skel_dilate, np.ones(erode_skel_20))
    skel_erode_5 = cv.erode(skel_dilate, np.ones(erode_skel_5))
    skel_erode_10 = cv.erode(skel_dilate, np.ones(erode_skel_10))


    # find the distance on the skeleton point.
    dist_on_skel = distance * skel_erode_10

    count_pos_dist = 0
    count_overone_dist = 0
    count_in_contour = 0

    # assign each skeleton to the correponding contour.
    points = defaultdict(list)  # [[x, y, val],]
    for i in range(len(dist_on_skel)):
        vals = dist_on_skel[i]
        for j in range(len(vals)):
            val = dist_on_skel[i][j]
            if val > 1:
                count_overone_dist += 1
            if val > 0:
                count_pos_dist += 1
                for idx_cnt in range(len(new_contours)):
                    res = cv.pointPolygonTest(new_contours[idx_cnt], (j, i), False)
                    dis = cv.pointPolygonTest(new_contours[idx_cnt], (j, i), True)
                    if res == 1:
                        count_in_contour += 1
                        points[idx_cnt].append([i, j, val, dis])
                        break

    print('=====================================')
    print('Local Width Stats of Each Tabacco Strand')

    response = []
    for point in points:
        stats = get_stats(points[point])
        print("Mean:", stats[0], "Var:", stats[1])
        response.append({'mean':stats[0]*2, 'var':stats[1]*4 })
    print('=====================================')

    result = {'response':response, 'files_info':images}
    return result



if __name__ == '__main__':
    image = cv.imread("image0.bmp")
    start(image)
