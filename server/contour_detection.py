
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from skimage import morphology,draw
from skimage.morphology import medial_axis
from collections import defaultdict
# import scipy.misc
# from remove_burr import Clain

"""


"""



def get_stats(point):
    dis = [None] * len(point)
    for i in range(len(point)):
        dis[i] = point[i][2]
    mean_dis = np.mean(dis)
    var_dis = np.var(dis)
    return [mean_dis, var_dis]









# fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3,  figsize=(12, 4))
#
#
# ax1.imshow(skel, cmap=plt.cm.gray)
# ax1.axis('off')
# ax1.set_title('skeleton', fontsize=20)
#
# ax2.imshow(distance, cmap=plt.cm.gray)
# ax2.axis('off')
# ax2.set_title('distance', fontsize=20)
#
# ax3.imshow(dist_on_skel, cmap=plt.cm.gray)
# ax3.axis('off')
# ax3.set_title('dist on skel', fontsize=20)
#
# fig.tight_layout()
# plt.show()

def start(image):
    # plt.imshow(image)
    # plt.title('Origin Image')
    # plt.show()
    images = []

    # convert to RGB
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    # create a binary thresholded image
    _, binary = cv.threshold(gray, 225, 255, cv.THRESH_BINARY_INV)
    # show it
    # plt.imshow(binary, cmap="gray")
    # plt.savefig('testplot.png')
    # plt.title('Binary Image')
    # plt.show()
    # cv.imwrite("binary.png", binary)
    images.append({'name':'binary version', 'filename':'binary.png', 'file':binary})

    # find the contours from the thresholded image
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # draw all contours
    # print(len(contours))
    max_area = -1
    max_area_idx = 0
    area_record = [0] * len(contours)
    for i in range(len(contours)):
        temp_area = cv.contourArea(contours[i])
        area_record[i] = temp_area
        if max_area < temp_area:
            max_area = temp_area
            max_area_idx = i

    contour_image = cv.drawContours(image, contours, -1, (0, 255, 0))
    # plt.imshow(contour_image)
    # plt.title('Origin Contour Image')
    # plt.show()
    images.append({'name':'origin contour', 'filename':'contour_init.png', 'file':contour_image})

    new_contours = []

    print('=====================================')
    print('Average Width of Each Tabacco Strand')

    for i in range(len(contours)):
        if area_record[i] >= max_area * 0.1 and area_record[i] <= max_area * 0.2:
            cnt = contours[i]
            new_contours.append(cnt)
            width_cnt = cv.contourArea(cnt) / cv.arcLength(cnt, True) * 2
            print('Avg Width: Area/arcLength * 2 : ', width_cnt)

            # rect = cv.minAreaRect(cnt)
            # box = cv.boxPoints(rect)
            # box = np.int0(box)
            # print(box)
            # cv.drawContours(img, [box], 0, (0, 0, 255), 2)
            # print('M: ',i)
            # print(cv.moments(contours[i]))
    # empty_image
    image[...] = 0

    image = cv.drawContours(image, new_contours, -1, (0, 255, 0), cv.FILLED)

    # plt.imshow(image)
    # plt.title('Selected Contours')
    # plt.show()
    images.append({'name':'selected contour', 'filename':'contour_selected.png', 'file':image})
    # convert to RGB
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    # create a binary thresholded image
    # _, binary = cv.threshold(gray, 225, 255, cv.THRESH_BINARY_INV)

    blur = ((5, 5), 1)
    erode_ = (10, 10)
    dilate_ = (20, 20)
    gray = cv.erode(cv.dilate(cv.GaussianBlur(gray, blur[0], blur[1]), np.ones(dilate_)), np.ones(erode_), 1)

    # plt.imshow(gray)
    # # plt.title('Edge Refined Contours')
    # plt.show()
    images.append({'name':'refined contour', 'filename':'contour_refined.png', 'file':gray})

    # plt.imshow(gray1)
    # plt.show()
    # plt.imshow(gray4)
    # plt.show()

    # skeleton =morphology.skeletonize(gray, method='lee')

    # print(len(contours))
    # show the image with the drawn contours

    # Compute the medial axis (skeleton) and the distance transform
    skel, distance = medial_axis(gray, return_distance=True)

    # plt.imshow(skel)
    # plt.title('Unprocessed Skeleton')
    # plt.show()

    # erode and dilate for skel
    erode_skel_20 = (20, 20)
    erode_skel_5 = (5, 5)
    erode_skel_10 = (10, 10)
    dilate_skel = (10, 10)

    skel_float = skel.astype(float)

    skel_dilate = cv.dilate(skel_float, np.ones(dilate_skel))
    skel_erode_20 = cv.erode(skel_dilate, np.ones(erode_skel_20))
    skel_erode_5 = cv.erode(skel_dilate, np.ones(erode_skel_5))
    skel_erode_10 = cv.erode(skel_dilate, np.ones(erode_skel_10))

    # plt.imshow(skel_erode_10)
    # plt.title('Processed Skeleton')
    # images.append({'name':'processed skeleton', 'filename':'skel_processed.png', 'file':skel_erode_10})

    # plt.show()

    dist_on_skel = distance * skel_erode_10

    count_pos_dist = 0
    count_overone_dist = 0
    count_in_contour = 0

    points = defaultdict(list)  # [[x, y, val],]
    for i in range(len(dist_on_skel)):
        vals = dist_on_skel[i]
        for j in range(len(vals)):
            val = dist_on_skel[i][j]
            if val > 1:
                count_overone_dist += 1
            if val > 0:
                count_pos_dist += 1
                # print(i, j, distance[i][j])
                for idx_cnt in range(len(new_contours)):
                    res = cv.pointPolygonTest(new_contours[idx_cnt], (j, i), False)
                    dis = cv.pointPolygonTest(new_contours[idx_cnt], (j, i), True)
                    # print(res)
                    if res == 1:
                        # print("In Contour", idx_cnt, dis)
                        count_in_contour += 1
                        points[idx_cnt].append([i, j, val, dis])
                        break
                    # else:
                    #     print("Out Contour", idx_cnt, dis)

    # plt.imshow(skel)
    # print(">0, ", count_pos_dist)
    # print(">1, ", count_overone_dist)
    # print("in contour, ", count_in_contour )

    # get stats
    print('=====================================')
    print('Local Width Stats of Each Tabacco Strand')

    response = []
    for point in points:
        # print(point)
        stats = get_stats(points[point])
        print("Mean:", stats[0], "Var:", stats[1])
        response.append({'mean':stats[0]*2, 'var':stats[1]*4 })
    print('=====================================')
    # extent = np.min(x), np.max(x), np.min(y), np.max(y)
    # fig = plt.figure(frameon=False)

    # plt.imshow(gray, cmap=plt.cm.gray, interpolation='nearest')
# 
    # plt.imshow(skel, cmap=plt.cm.viridis, alpha=.9, interpolation='bilinear')

    # plt.title('Skeleton in Gray Image')
    # plt.show()
    result = {'response':response, 'files_info':images}
    return result
    #



if __name__ == '__main__':
    image = cv.imread("image0.bmp")
    start(image)
