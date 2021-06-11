import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import tkinter
img = cv.imread('page1.jpg', 0)
img2 = img.copy()
template = cv.imread('page0.jpg', 0)
w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
# 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED','cv.TM_CCOEFF', , 'cv.TM_CCORR'
methods = ['cv.TM_CCOEFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    image = img[top_left[1] + h:, :top_left[0] + w]
    # image = cv.resize(image, (700, 900))
    cv.imwrite('upper_part_crop.jpg', image)
    cv.imshow('before resize', image)

    # second_image = cv.imread('J1534-12_copy.jpg', 0)
    # cv.imshow('second', second_image)
    # result = cv.matchTemplate(imageGr, second_image, method)
    # (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(result)
    # # (startX, startY) = maxLoc
    # # endX = startX + template.shape[1]
    # # endY = startY + template.shape[0]
    # cv.rectangle(img, (startX, startY), (endX, endY), (255, 0, 0), 3)

    # # print(type(image))
    # color_var = (0, 0, 255)
    # cv.rectangle(img, top_left, bottom_right, color_var, 3)
    # cv.imshow('crop', image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # plt.subplot(121), plt.imshow(img, cmap='Reds')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(image, cmap='rainbow')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(meth)
    # plt.show()
