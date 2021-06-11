# from pdf2image import convert_from_path
# import os
#
# poppler_path = '/home/abs/Desktop/textract_file/office_work/poppler-21.03.0/Library/bin/'
#
#
# def pdf_to_image(pdf_path, dir_name=None):
#
#     try:
#         images = convert_from_path(pdf_path, poppler_path=poppler_path)
#
#         if dir_name is None:
#             dir_name = "_".join(pdf_path.split('/')[-1].split('.')[:-1])
#         print(dir_name)
#
#         if not os.path.exists(dir_name):
#             os.makedirs(dir_name)
#
#         for i in range(len(images)):
#             images[i].save(dir_name + '/page' + str(i+1) + '.jpg', 'JPEG')
#
#         return dir_name, len(images)
#
#     except Exception as err:
#         return None, 0
#
#
# pdf_img_dir, pages = pdf_to_image("EXP-2144.pdf")
# if pdf_img_dir is not None:
#     print('PDF converted to images')


# import module
from pdf2image import convert_from_path
import cv2


# Store Pdf with convert_from_path function
images = convert_from_path('JK2_21_05.pdf')

for i in range(len(images)):
    # Save pages as images in the pdf
    images[i].save(f'JK2_21_05{i}' + '.jpg', 'JPEG')

image = cv2.imread('JK2_21_050.jpg')
result = image.copy()
result1 = cv2.resize(result,(900, 1080))
cv2.imshow('original_image', result1)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray_image,0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imshow('thresh_image', thresh)

#Horizontal lines removal
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(result, [c], -1, (255,255,255), 5)

#Vertical lines removal
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(result, [c], -1, (255,255,255), 5)

cv2.imshow('result_image1', result)
cv2.imwrite('JK2_21_050_result.jpg', result)
cv2.waitKey()


