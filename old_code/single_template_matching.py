# USAGE
# python single_template_matching.py --image images/coke_bottle.png --template images/coke_logo.png

# import the necessary pages
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input image where we'll apply template matching", default='J1534-12.jpg')
ap.add_argument("-t", "--template", type=str, required=True,
                help="path to template image", default='J1534-1.jpg')
args = vars(ap.parse_args())

# load the input image and template image from disk, then display
# them to  our screen
print("[INFO] loading images...")
image = cv2.imread(args["image"])
template = cv2.imread(args["template"])
# cv2.imshow("Image", image)
# cv2.imshow("Template", template)

# convert both the image and template to grayscale
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
w, h = templateGray.shape[::-1]
# perform template matching
print("[INFO] performing template matching...")
result = cv2.matchTemplate(imageGray, templateGray,
                           cv2.TM_CCOEFF_NORMED)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

# determine the starting and ending (x, y)-coordinates of the
# bounding box

(startX, startY) = maxLoc
endX = startX + template.shape[1]
endY = startY + template.shape[0]
top_left = minLoc
# draw the bounding box on the image
# cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 3)
# cv2.imshow("Output1", image)
bottom_right = (top_left[0] + w, top_left[1] + h)
image = image[top_left[1] + h:, :top_left[0] + w]
# image = cv2.resize(image, (700, 900))
# show the output image
cv2.imshow("Output", image)
second_image = cv2.imread('J1534-12_copy.jpg')
second_image = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)
cv2.imshow('second', imageGray)
cv2.waitKey(0)
w, h = second_image.shape[::-1]
print(image.shape)
result1 = cv2.matchTemplate(imageGray, second_image,
                            cv2.TM_CCOEFF_NORMED)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result1)
(startX, startY) = maxLoc
endX = startX + template.shape[1]
endY = startY + template.shape[0]
print(endX, endY)
top_left = minLoc
imageGray = cv2.rectangle(imageGray, (startX, startY),
                          (endX, endY), (255, 0, 0), 3)
imageGray = cv2.resize(imageGray, (600, 900))
cv2.imshow('final', imageGray)
cv2.waitKey(0)
bottom_right = (top_left[0] + w, top_left[1] + h)
image1 = image[top_left[1] + h:, :top_left[0] + w]
# cv2.imshow('final', image1)
# cv2.waitKey(0)
