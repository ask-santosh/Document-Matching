import easyocr
import cv2
reader = easyocr.Reader(['en'], gpu=False)
import numpy as np

# result = reader.readtext('test.jpg')
img = cv2.imread('page_1.jpg')
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# retval, thresh = cv2.threshold(gray_img, 127, 255, 0)
# img_contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# img1 = cv2.drawContours(img, img_contours, -2, (0, 255, 0))
result1 = cv2.fastNlMeansDenoisingColored(img,None,20,10,7,21)
edge_img = cv2.Canny(result1,400,400)
vertical = np.uint8(np.absolute(cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=1)))
horizon = np.uint8(np.absolute(cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=1)))
Sobel = cv2.bitwise_or(vertical, horizon)


result = reader.readtext(edge_img)
for rst in result:
    print(rst)
cv2.imshow('Image Contours', edge_img)
cv2.imshow('sobel', Sobel)
cv2.waitKey(0)


# print(result[1])
# lst2 = [item[1] for item in result]
# print(lst2)
# test_string = result.decode('utf-8')
# file1 = open('JK2_21_050.txt', 'w')
# file1.write(str(lst2))
# file1.close()